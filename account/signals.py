from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile  # Assuming you have a Profile model

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:  # Only create a profile when a new user is created
        Profile.objects.create(user=instance)  # Assuming Profile has a OneToOne field to User
    else:  # Save the existing profile if the user is being updated
        instance.profile.save()
 