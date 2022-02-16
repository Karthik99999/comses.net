# Generated by Django 2.0.4 on 2018-04-03 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0002_auto_20150616_2121"),
    ]

    operations = [
        migrations.CreateModel(
            name="TagCleanup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("new_name", models.CharField(blank=True, max_length=300)),
                ("old_name", models.CharField(max_length=300)),
            ],
            options={
                "permissions": (("process", "Able to process tag cleanups"),),
            },
        ),
        migrations.CreateModel(
            name="TagCleanupTransaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="TagCuratorProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
            },
            bases=("taggit.tag",),
        ),
        migrations.AddField(
            model_name="tagcleanup",
            name="transaction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="curator.TagCleanupTransaction",
            ),
        ),
    ]
