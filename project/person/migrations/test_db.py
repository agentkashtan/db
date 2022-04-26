from django.db import migrations, models
import django.db.models.deletion


def create_db(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    db = apps.get_model("person", "ReadOnlyDB")
    db.objects.using(db_alias).create(key=228)


class Migration(migrations.Migration):

    dependencies = [
         ('person', '0002_persontodelete_unconfirmedtransaction_and_more'),
    ]

    operations = [
        migrations.RunPython(create_db),
    ]