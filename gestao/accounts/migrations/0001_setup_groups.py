from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


def setup_groups(apps, schema_editor):
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    gestor_group, _ = Group.objects.get_or_create(name='Gestor')
    engenheiro_group, _ = Group.objects.get_or_create(name='Engenheiro')

    all_perms = Permission.objects.all()
    admin_group.permissions.set(all_perms)

    gestor_perms = Permission.objects.filter(
        content_type__app_label__in=['crm', 'projects'],
        codename__in=[
            'view_client', 'add_client', 'change_client',
            'view_project', 'add_project', 'change_project',
            'view_projectstage', 'add_projectstage', 'change_projectstage',
        ]
    )
    gestor_perms |= Permission.objects.filter(
        content_type__app_label='financial',
        codename__in=[
            'view_quote', 'add_quote', 'change_quote',
            'view_payment', 'add_payment', 'change_payment',
            'view_cashflow', 'add_cashflow', 'change_cashflow',
        ]
    )
    gestor_group.permissions.set(gestor_perms)

    engenheiro_perms = Permission.objects.filter(
        content_type__app_label__in=['crm', 'projects'],
        codename__in=[
            'view_client',
            'view_project',
            'view_projectstage', 'add_projectstage', 'change_projectstage',
        ]
    )
    engenheiro_group.permissions.set(engenheiro_perms)


def remove_groups(apps, schema_editor):
    Group.objects.filter(name__in=['Admin', 'Gestor', 'Engenheiro']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crm', '0001_initial'),
        ('projects', '0001_initial'),
        ('financial', '0002_companysettings_cashflow'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_groups, remove_groups),
    ]
