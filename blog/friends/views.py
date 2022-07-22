from django.http import HttpRequest
from django.shortcuts import render
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .utils import get_friends_birthdays, get_user_friendlist


@login_required
def friends(request: HttpRequest):
    user_session_id: str = str(request.user.profile.id)

    # OPTIMIZE
    suggestions = list(
        filter(lambda user: str(user.id) != user_session_id, Profile.objects.all())
    )

    return render(request, 'friends/friends.html', {
        'friends': suggestions
    })


@login_required
def friend_requests(request: HttpRequest):
    user: Profile = Profile.objects.get(id=request.user.profile.id)

    friend_requests: list = get_user_friendlist(user.friend_requests)

    return render(request, 'friends/friend-requests.html', {
        'friend_requests': friend_requests,
        'user': user
    })


@login_required
def sent_friend_requests(request: HttpRequest):
    user: Profile = Profile.objects.get(id=request.user.profile.id)

    sent_friend_requests: list = get_user_friendlist(user.sent_friend_requests)

    return render(request, 'friends/sent-friendrequests.html', {
        'sent_friend_requests': sent_friend_requests
    })


@login_required
def friend_suggestions(request: HttpRequest):
    user_session_id: str = request.user.profile.id

    # OPTIMIZE
    suggestions = list(
        filter(lambda user: user.id != user_session_id, Profile.objects.all())
    )

    return render(request, 'friends/friend-suggestions.html', {
        'suggestions': suggestions
    })


@login_required
def friends_all(request: HttpRequest, user_username: str):
    user: Profile = User.objects.get(username=user_username).profile # OPTIMIZE

    all_friends: list = get_user_friendlist(user.friends)

    return render(request, 'friends/friends-all.html', {
        'all_friends': all_friends,
        'profile': user,
        'profile_name': user.name.split(" ")[0]
    })


@login_required
def friends_birthdays(request: HttpRequest):
    user: Profile = Profile.objects.get(id=request.user.profile.id)

    birthdays: dict = get_friends_birthdays(user)

    return render(request, 'friends/friends-birthdays.html', {
        'birthdays': birthdays
    })


@login_required
def close_friends(request: HttpRequest):
    user: Profile = Profile.objects.get(id=request.user.profile.id) # OPTIMIZE

    close_friends: list = get_user_friendlist(user.close_friends)

    return render(request, 'friends/close-friends.html', {
        'close_friends': close_friends
    })