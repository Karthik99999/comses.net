# Generated by Django 2.0.4 on 2018-04-07 00:23

import core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_order_by_name_for_journal_and_platform"),
    ]

    operations = [
        migrations.AddField(
            model_name="journal",
            name="_description_rendered",
            field=models.TextField(default="foo", editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="journal",
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
            model_name="journal",
            name="description",
            field=core.fields.MarkdownField(
                blank=True, max_length=1000, rendered_field=True
            ),
        ),
    ]
