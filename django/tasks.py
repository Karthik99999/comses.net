from invoke import task
from invoke.tasks import call

import logging
import os
import sys


# push current working directory onto the path to access core.settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

from django.conf import settings

env = {
    'python': 'python3',
    'project_name': 'cms',
    'db_name': settings.DATABASES['default']['NAME'],
    'db_host': settings.DATABASES['default']['HOST'],
    'db_user': settings.DATABASES['default']['USER'],
    'project_conf': os.environ.get('DJANGO_SETTINGS_MODULE'),
    'coverage_omit_patterns': ('test', 'settings', 'migrations', 'wsgi', 'management', 'tasks', 'apps.py'),
    'coverage_src_patterns': ('home', 'library', 'core',),
}

logger = logging.getLogger(__name__)


def dj(ctx, command, **kwargs):
    """
    Run a Django manage.py command on the server.
    """
    ctx.run('{python} manage.py {dj_command} --settings {project_conf}'.format(dj_command=command, **env),
            **kwargs)


@task
def clean_update(ctx):
    ctx.run("git fetch --all && git reset --hard origin/master")


@task
def clean(ctx, revert=False):
    ctx.run("find . -name '*.pyc' -o -name 'generated-*' -delete -print")
    if revert:
        clean_update(ctx)


@task
def sh(ctx):
    dj(ctx, 'shell_plus --ipython', pty=True)


@task
def test(ctx, name=None, coverage=False):
    if name is not None:
        apps = name
    else:
        apps = ''
    if coverage:
        ignored = ['*{0}*'.format(ignored_pkg) for ignored_pkg in env['coverage_omit_patterns']]
        coverage_cmd = "coverage run --source={0} --omit={1}".format(','.join(env['coverage_src_patterns']),
                                                                     ','.join(ignored))
    else:
        coverage_cmd = env['python']
    ctx.run('{coverage_cmd} manage.py test {apps}'.format(apps=apps, coverage_cmd=coverage_cmd))


@task(pre=[call(test, coverage=True)])
def coverage(ctx):
    ctx.run('coverage html')


@task
def server(ctx, ip="0.0.0.0", port=8000):
    dj(ctx, 'runserver {ip}:{port}'.format(ip=ip, port=port), capture=False)

@task(aliases=['ss'])
def setup_site(ctx, site_name='CoMSES Net',
               site_domain='localhost'):
    dj(ctx, 'setup_site --site-name="{0}" --site-domain="{1}"'.format(site_name, site_domain))

@task(aliases=['idd'])
def import_drupal_data(ctx, directory='incoming'):
    dj(ctx, 'import_drupal_data -d {0}'.format(directory))

@task(aliases=['icf'])
def import_codebase_files(ctx, directory='incoming/models'):
    dj(ctx, 'import_codebase_files -d {0}'.format(directory))


@task(import_drupal_data, import_codebase_files, aliases=['ima'])
def import_all(ctx):
    pass

'''
@task(aliases=['rfd'])
def restore_from_dump(ctx, dumpfile='dump.sql', init_db_schema=True, force=False):
    import django
    django.setup()
    from citation.models import Publication
    number_of_publications = 0
    try:
        number_of_publications = Publication.objects.count()
    except:
        pass
    if number_of_publications > 0 and not force:
        print("Ignoring restore, database with {0} publications already exists. Use --force to override.".format(number_of_publications))
    else:
        create_pgpass_file(ctx)
        ctx.run('dropdb -w --if-exists -e {db_name} -U {db_user} -h db'.format(**env), echo=True, warn=True)
        ctx.run('createdb -w {db_name} -U {db_user} -h db'.format(**env), echo=True, warn=True)
        if os.path.isfile(dumpfile):
            logger.debug("loading data from %s", dumpfile)
            ctx.run('psql -w -q -h db {db_name} {db_user} < {dumpfile}'.format(dumpfile=dumpfile, **env),
                    warn=True)
    if init_db_schema:
        initialize_database_schema(ctx)
'''


@task(aliases=['pgpass'])
def create_pgpass_file(ctx, force=False):
    pgpass_path = os.path.join(os.path.expanduser('~'), '.pgpass')
    if os.path.isfile(pgpass_path) and not force:
        return
    with open(pgpass_path, 'w+') as pgpass:
        db_password = settings.DATABASES['default']['PASSWORD']
        pgpass.write('db:*:*:{db_user}:{db_password}\n'.format(db_password=db_password, **env))
        ctx.run('chmod 0600 ~/.pgpass')

@task
def backup(ctx, path='/backups/postgres'):
    create_pgpass_file(ctx)
    ctx.run('/code/deploy/backup/autopgsqlbackup.sh -c /code/deploy/backup/autopgsqlbackup.conf')


@task(aliases=['idb', 'initdb'])
def initialize_database_schema(ctx, clean=False):
    if clean:
        for app in ('home', 'library'):
            migration_dir = os.path.join(app, 'migrations')
            ctx.run('find {0} -name 00*.py -delete -print'.format(migration_dir))
    dj(ctx, 'makemigrations home library')
    dj(ctx, 'migrate --noinput')


@task(aliases=['rdb', 'resetdb'])
def reset_database(ctx):
    create_pgpass_file(ctx)
    ctx.run('psql -h {db_host} -c "alter database {db_name} connection limit 1;" -w {db_name} {db_user}'.format(**env),
            echo=True, warn=True)
    ctx.run('psql -h {db_host} -c "select pg_terminate_backend(pid) from pg_stat_activity where datname=\'{db_name}\'" -w {db_name} {db_user}'.format(**env),
            echo=True, warn=True)
    ctx.run('dropdb -w --if-exists -e {db_name} -U {db_user} -h {db_host}'.format(**env), echo=True, warn=True)
    ctx.run('createdb -w {db_name} -U {db_user} -h {db_host}'.format(**env), echo=True, warn=True)
    initialize_database_schema(ctx, False)
