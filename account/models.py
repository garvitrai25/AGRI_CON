from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICE= (('M','Male'),('F','Female'),('OG','Other'))
    profile_pic = models.ImageField(upload_to='profilepic', null=True, blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE,blank=True)
    address = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    USER_TYPE= (('S','Saller'),('B','Buyer'))
    user_type = models.CharField(max_length=10,choices=USER_TYPE,blank=False)

    def __str__(self):
        return self.user.username

# Signal to create User_info when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a User_info instance for every new User created."""
    if created:
        # Check if a User_info already exists for this user
        if not User_info.objects.filter(user=instance).exists():
            try:
                User_info.objects.create(
                    user=instance,
                    gender='M',
                    address='Your Address',
                    phone='Your Phone Number',
                    user_type='B',
                    profile_pic='profilepic/default.jpg'
                )
                print(f"Created User_info for {instance.username}")
            except Exception as e:
                print(f"Error creating User_info for {instance.username}: {e}")