from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0008_contactmessage_alter_profile_role")]

    operations = [
        migrations.CreateModel(
            name="MarketPriceSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cache_key", models.CharField(db_index=True, max_length=64, unique=True)),
                ("filters", models.JSONField(blank=True, default=dict)),
                ("payload", models.JSONField(blank=True, default=list)),
                ("fetched_at", models.DateTimeField(auto_now=True)),
                ("reporting_date", models.DateField(blank=True, null=True)),
                ("source_title", models.CharField(blank=True, default="AGMARKNET / data.gov.in", max_length=255)),
            ],
        ),
    ]
