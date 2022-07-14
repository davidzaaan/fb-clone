from users.models import Profile

def exists(friend_id: str) -> bool:
    """
        Function that filters non-existing friends from the user given friends list
        :param friend_id: String containing the id of the user to check if still exists
        :param user: Profile object containing the current user session profile
        :return bool:
    """
    try:
        profile: Profile = Profile.objects.get(id=friend_id) # OPTIMIZE
        return profile
    except Profile.DoesNotExist:
        return None


def get_user_friendlist(user_list: Profile) -> list:
    """
        Function that returns the given user friend list
        :param user: Profile object to obtain the friend list
        :return list: Profile object list containing all the user friends
    """
    friends_list: list = []

    if not len(user_list) > 0:
        return None

    for friend_id in user_list:
        friend: Profile = exists(friend_id)
        
        if friend:
            friends_list.append(friend)

    return friends_list


def get_friends_birthdays(user: Profile) -> dict:
    """
    Function that returns a dictionary with all the months of the year with the user friends birthdays 
    in each key
    :param user: Profile object containing to get the friends list and access to their birthdays
    :return dict: Dictionary with all the classified birthdays and friends
    """
    months: dict = {
        "January": [], "February": [], "March": [], 
        "April": [], "May": [], "June": [], "July": [], 
        "August": [], "September": [], "October": [],
        "November": [], "December": []
    }

    friends: list = get_user_friendlist(user.friends)

    for friend in friends:
        # month of the current friend birth date
        bthday_month: str = friend.birthday.strftime("%B")
        if not friend in months[bthday_month]:
            months[bthday_month].append(friend)

    months = {month: friend_list for month, friend_list in months.items() if len(friend_list) > 0}

    return months        