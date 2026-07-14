from django.db import migrations


def clean_seed_clientes(apps, schema_editor):
    Client = apps.get_model('crm', 'Client')
    nomes = [
        'Muhalaze', 'Katembe', '2ª Rotunda', 'Matlemele',
        'Família Guava', 'Manuel Chimututo', 'Inoque João Cesar',
        'Venestâncio Tomás Cossa',
    ]
    Client.objects.filter(nome__in=nomes).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clean_seed_clientes),
    ]
