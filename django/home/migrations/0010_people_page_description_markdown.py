# Generated by Django 2.1.3 on 2018-11-15 18:00

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_people_terms"),
    ]

    operations = [
        migrations.AddField(
            model_name="peoplepage",
            name="_description_rendered",
            field=models.TextField(default="", editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="peoplepage",
            name="description_markup_type",
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
        migrations.AlterField(
            model_name="peoplepage",
            name="description",
            field=core.fields.MarkdownField(
                blank=True,
                help_text="Text blurb on the people leading comses.net",
                rendered_field=True,
            ),
        ),
    ]
