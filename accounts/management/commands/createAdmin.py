from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = "Create System user."

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email="admin@sinh.com")
        except User.DoesNotExist:
            user = User.objects.create(username="admin@sinh.com",email="admin@sinh.com",first_name="Sinh", last_name="Salon")
            user.set_password("Sinh@1234")
            user.save()
            user_profile = UserProfile.objects.create(user=user, user_type=0, address="NA")
            user_profile.save()
    
        self.stdout.write(
            self.style.SUCCESS('Successfully created admin user')
        )
