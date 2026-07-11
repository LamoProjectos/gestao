from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria ou actualiza os utilizadores iniciais do sistema'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username='admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.set_password('56510')
        admin.email = 'admin@lamoprojectos.com'
        admin.save()
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
        if created:
            self.stdout.write(self.style.SUCCESS('Eng criado: eng / 1234'))
        else:
            self.stdout.write(self.style.SUCCESS('Eng actualizado: eng / 1234'))
