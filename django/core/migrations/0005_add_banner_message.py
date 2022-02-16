# Generated by Django 2.2.6 on 2019-10-07 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_memberprofile_longer_bio_research_interests"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="banner_destination_url",
            field=models.URLField(
                blank=True, help_text="URL to redirect to when this banner is clicked"
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="banner_message",
            field=models.TextField(
                blank=True, help_text="Notification message to display to all users"
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
