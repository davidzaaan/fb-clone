# Create the signals for when a new User is registered, a new Profile will be created automatically
from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def create_profile(sender, **kwargs):
    print("PRE profile signal trigered")
    print(kwargs)
    # Create new profile


@receiver(post_save, sender=Profile)
def post_save_signal(sender, **kwargs):
    print("POST SAVE")
    print(kwargs)
    user = kwargs['instance']





# post_save.connect(create_profile, sender=User)
# pre_save.connect(create_profile, sender=User)
# post_save.connect(sapo, sender=User)