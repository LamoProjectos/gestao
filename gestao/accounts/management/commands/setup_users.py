from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Cria ou actualiza os utilizadores iniciais do sistema'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        gestor_group, _ = Group.objects.get_or_create(name='Gestor')
        engenheiro_group, _ = Group.objects.get_or_create(name='Engenheiro')

        admin, created = User.objects.get_or_create(username='admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.set_password('56510')
        admin.email = 'admin@lamoprojectos.com'
        admin.save()
        admin.groups.add(admin_group)
        if created:
            self.stdout.write(self.style.SUCCESS('Admin criado: admin / 56510'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin actualizado: admin / 56510'))

        eng, created = User.objects.get_or_create(username='eng')
        eng.first_name = 'Engenheiro'
        eng.is_staff = True
        eng.set_password('1234')
        eng.email = 'eng@lamoprojectos.com'
        eng.save()
        eng.groups.add(engenheiro_group)
        if created:
            self.stdout.write(self.style.SUCCESS('Eng criado: eng / 1234'))
        else:
            self.stdout.write(self.style.SUCCESS('Eng actualizado: eng / 1234'))
