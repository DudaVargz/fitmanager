import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fitmanager.com', 'fitmanager123')
    print('Superusuário criado!')
else:
    print('Já existe.')