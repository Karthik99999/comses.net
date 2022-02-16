import csv
import logging
import sys

import pytz
from dateutil.parser import parse as parse_date
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import ComsesGroups

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Dump active member profiles with optional date_joined filter --after=yyyy-mm-dd"

    def add_arguments(self, parser):
        parser.add_argument(
            "--full-member-only", "-u", action="store_true", dest="full_member_only"
        )
        parser.add_argument(
            "--after",
            "-a",
            action="store",
            dest="after",
            default=None,
            help="yyyy-mm-dd date after which users were added e.g., --after=2018-03-15",
        )

    def handle(self, *args, **options):
        # exclude django-guardian AnonymousUser
        User = get_user_model()
        anonymous_user = User.get_anonymous()
        criteria = {"is_active": True}
        after_string = options["after"]
        if after_string is not None:
            after_date = parse_date(after_string).replace(tzinfo=pytz.UTC)
            criteria.update(date_joined__gte=after_date)
        full_member = options["full_member_only"]
        qs = (
            ComsesGroups.FULL_MEMBER.users(**criteria)
            if full_member
            else User.objects.filter(**criteria).exclude(pk=anonymous_user.pk)
        )
        csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=[
                "last_name",
                "first_name",
                "email",
                "date_joined",
                "bio",
                "institution",
                "degrees",
                "orcid_url",
                "github_url",
                "research_interests",
                "affiliations",
            ],
        )
        csv_writer.writeheader()
        for user in qs:
            mp = user.member_profile
            csv_writer.writerow(
                {
                    "last_name": user.last_name,
                    "first_name": user.first_name,
                    "email": user.email,
                    "date_joined": user.date_joined,
                    "bio": mp.bio,
                    "research_interests": mp.research_interests,
                    "institution": mp.institution,
                    "degrees": mp.degrees,
                    "affiliations": mp.affiliations,
                    "orcid_url": mp.orcid_url,
                    "github_url": mp.github_url,
                }
            )
