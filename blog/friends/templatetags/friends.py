from django import template
from users.models import Profile

register = template.Library()

@register.filter(name="has_sent_a_fr")
def has_sent_a_fr(user_id, friend_id):
    # Always convert the UUID object to str, otherwise the filter wont work properly
    user_profile: Profile = Profile.objects.get(id=user_id) # OPTIMZE
    return str(friend_id) in user_profile.sent_friend_requests


@register.filter(name="is_in_fr")
def is_in_fr(user_id, friend_id):
    user_profile: Profile = Profile.objects.get(id=user_id) # OPTIMZE
    return str(friend_id) in user_profile.friend_requests


@register.filter(name="is_friend")
def is_friend(user_id, friend_id):
    user_profile: Profile = Profile.objects.get(id=user_id) # OPTIMZE
    print(user_profile.friends)
    return str(friend_id) in user_profile.friends


@register.filter(name="is_closefriend")
def is_closefriend(user_id, friend_id):
    user_profile: Profile = Profile.objects.get(id=user_id) # OPTIMZE
    return str(friend_id) in user_profile.close_friends