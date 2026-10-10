import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User

def reset():
    # 1. Update/Ensure admin superuser
    admin, created = User.objects.get_or_create(username='admin')
    admin.email = 'admin@codealpha.tech'
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.is_active = True
    admin.save()
    print("✅ Superuser 'admin' updated/verified with password 'admin123' and email 'admin@codealpha.tech'.")

    # 2. Also ensure a user with username='admin@codealpha.tech' exists as superuser if typed in username field
    admin_email_user, created2 = User.objects.get_or_create(username='admin@codealpha.tech')
    admin_email_user.email = 'admin@codealpha.tech'
    admin_email_user.set_password('admin123')
    admin_email_user.is_staff = True
    admin_email_user.is_superuser = True
    admin_email_user.is_active = True
    admin_email_user.save()
    print("✅ Superuser 'admin@codealpha.tech' updated/verified with password 'admin123'.")

if __name__ == '__main__':
    reset()
