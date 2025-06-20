"""
Management command for indexing digest archives based on the contents of home/static/digest/

Follow the formatting convention of the existing files in home/static/digest/:
e.g. vol11_no3_Spring_2023.pdf
"""

import logging
import re
import requests
from datetime import datetime
from django.core.management.base import BaseCommand

from home.models import ComsesDigest

logger = logging.getLogger(__name__)

ZENODO_COMMUNITY_API_URL = "https://zenodo.org/api/communities/comses-digest/records"


class Command(BaseCommand):
    help = "Update CoMSES digest archives page based on the contents of home/static/digest/"

    def handle(self, *args, **options):
        ComsesDigest.objects.all().delete()

        response = requests.get(ZENODO_COMMUNITY_API_URL)
        if response.status_code != 200:
            logger.error("Failed to fetch Zenodo records for CoMSES Digest.")
            return

        zenodo_records = response.json()["hits"]["hits"]
        for record in zenodo_records:
            file_name = record["files"][0]["key"]
            if file_name.endswith(".pdf"):
                try:
                    self.add_digest_archive(file_name, record["links"]["latest_html"])
                except Exception as e:
                    logger.error(e)
            else:
                logger.info(f"Skipping non-pdf file: {file_name}")

        logger.info(f"\n\nSuccessfully indexed all pdfs from Zenodo community.")

    def add_digest_archive(self, file_name, url):
        # FIXME: consider rolling all these regex searches into a single-pass regex monstrosity
        volume = int(re.search(r"vol(\d+)", file_name, re.IGNORECASE).group(1))
        issue_number = int(re.search(r"no(\d+)", file_name, re.IGNORECASE).group(1))
        date_str = re.search(r"(\d{2}-\d{2}-\d{4})", file_name).group(1)
        publication_date = datetime.strptime(date_str, "%m-%d-%Y").date()
        season_str = (
            re.search(r"(spring|summer|fall|winter)", file_name, re.IGNORECASE)
            .group(1)
            .upper()
        )
        season = ComsesDigest.Seasons[season_str]
        digest = ComsesDigest.objects.create(
            volume=volume,
            issue_number=issue_number,
            publication_date=publication_date,
            season=season,
            url=url,
        )
        logger.info(digest)
