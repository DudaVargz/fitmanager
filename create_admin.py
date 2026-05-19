import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.all().delete()
User.objects.create_superuser('admin', 'admin@fitmanager.com', 'fitmanager123')
print('Superusuário criado com sucesso!')