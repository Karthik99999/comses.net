# Generated by Django 2.2.4 on 2019-08-03 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0009_rename_platform_to_framework"),
    ]

    operations = [
        migrations.AlterField(
            model_name="peerreviewerfeedback",
            name="has_clean_code",
            field=models.BooleanField(
                default=False,
                help_text="Is the code clean, well-written, and well-commented with consistent formatting? (A checked box indicates that the model code is clean)",
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewerfeedback",
            name="has_narrative_documentation",
            field=models.BooleanField(
                default=False,
                help_text="Is there sufficiently detailed accompanying narrative documentation? (A checked box indicates that the model has narrative documentation)",
            ),
        ),
        migrations.AlterField(
            model_name="peerreviewerfeedback",
            name="is_runnable",
            field=models.BooleanField(
                default=False,
                help_text="Were you able to run the model with the provided instructions? (A checked box indicates that the model is runnable)",
            ),
        ),
    ]
