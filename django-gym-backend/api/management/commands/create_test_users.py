from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from api.models import User, Role, Gender, Goal, Level

class Command(BaseCommand):
    help = 'Test kullanıcıları oluşturur'

    def handle(self, *args, **options):
        # Admin kullanıcısı
        admin_user, created = User.objects.get_or_create(
            username='admin',
            email='admin@example.com',
            defaults={
                'password': make_password('admin123'),
                'first_name': 'Admin',
                'last_name': 'User',
                'role': Role.ADMIN,
                'is_active': True,
                'gender': Gender.MALE,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        # Eğer kullanıcı zaten varsa, is_active alanını güncelle
        if not created:
            admin_user.is_active = True
            admin_user.save()
            self.stdout.write(self.style.WARNING(f'Admin kullanıcısı güncellendi: {admin_user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Admin kullanıcısı oluşturuldu: {admin_user.email}'))
        
        # Eğitmen kullanıcısı
        trainer_user, created = User.objects.get_or_create(
            username='trainer',
            email='trainer@example.com',
            defaults={
                'password': make_password('trainer123'),
                'first_name': 'Trainer',
                'last_name': 'User',
                'role': Role.TRAINER,
                'is_active': True,
                'gender': Gender.MALE,
                'admin': admin_user,
            }
        )
        
        # Eğer kullanıcı zaten varsa, is_active alanını güncelle
        if not created:
            trainer_user.is_active = True
            trainer_user.save()
            self.stdout.write(self.style.WARNING(f'Eğitmen kullanıcısı güncellendi: {trainer_user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Eğitmen kullanıcısı oluşturuldu: {trainer_user.email}'))
        
        # Normal kullanıcı
        user, created = User.objects.get_or_create(
            username='user',
            email='user@example.com',
            defaults={
                'password': make_password('user123'),
                'first_name': 'Normal',
                'last_name': 'User',
                'role': Role.USER,
                'is_active': True,
                'gender': Gender.FEMALE,
                'age': 25,
                'height': 170,
                'weight': 65,
                'goal': Goal.LOSE_WEIGHT,
                'level': Level.BEGINNER,
                'admin': admin_user,
                'trainer': trainer_user,
            }
        )
        
        # Eğer kullanıcı zaten varsa, is_active alanını güncelle
        if not created:
            user.is_active = True
            user.save()
            self.stdout.write(self.style.WARNING(f'Normal kullanıcı güncellendi: {user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Normal kullanıcı oluşturuldu: {user.email}')) 