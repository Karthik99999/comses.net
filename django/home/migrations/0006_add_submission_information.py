# Generated by Django 2.0.5 on 2018-05-17 22:30

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_add_conference_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="conferencepage",
            name="_submission_information_rendered",
            field=models.TextField(default="", editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="conferencepage",
            name="submission_information",
            field=core.fields.MarkdownField(
                blank=True,
                help_text="Markdown formatted info on how to submit a presentation to the conference",
                rendered_field=True,
            ),
        ),
        migrations.AddField(
            model_name="conferencepage",
            name="submission_information_markup_type",
            field=models.CharField(
                choices=[
                    ("", "--"),
                    ("markdown", "markdown"),
                    ("html", "html"),
                    ("plain", "plain"),
                    ("", ""),
                ],
                default="markdown",
                max_length=30,
            ),
        ),
    ]
