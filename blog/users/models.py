from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
    name = models.CharField(max_length=180)
    email = models.EmailField(max_length=150)
    bio = models.CharField(max_length=70, null=True, blank=True)
    birthday = models.DateField(null=True, editable=True, default=now)
    created = models.DateTimeField(auto_now_add=True)
    # password = models.CharField(max_length=180)
    profile_photo = models.ImageField(null=True, blank=True, upload_to='profiles/', default='default/default_profile.jpg')
    cover_photo = models.ImageField(null=True, blank=True, upload_to='coverphotos/', default='default/default_cover.jpg')
    videos = models.FileField(upload_to='videos', null=True, blank=True)
    friends = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )
    close_friends = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )
    friend_requests = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )
    sent_friend_requests = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    
    def add_friend(self, friend_id: str) -> None:
        """
            Function that adds the given string id to the friends list
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to add to the friends list
            :return: None
        """
        if not friend_id in self.friends:
            self.friends.append(friend_id)
            self.save()

    
    def remove_friend(self, friend_id: str) -> None:
        """
            Function that removes the given string id from the friends list
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to remove from the friends list
            :return: None
        """
        if friend_id in self.friends:
            self.friends.remove(friend_id)
            self.save()

    
    def get_friends_count(self) -> int:
        """
            Function that returns the total numbers of friends
            :param self: Instance of the present model
            :return: int
        """
        return len(self.friends)

    
    def add_friend_request(self, friend_id: str) -> None:
        """
            Function that adds the given string id to the friend_requests list
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to add to the friend_requests list
            :return: None
        """
        if not friend_id in self.friend_requests:
            self.friend_requests.append(friend_id)
            self.save()

    
    def remove_fr(self, friend_id: str) -> None:
        """
            Function that removes the given string id from the friend_requests list
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to remove from the friend_requests list
            :return: None
        """
        if friend_id in self.friend_requests:
            self.friend_requests.remove(friend_id)
            self.save()


    def add_to_sent_fr(self, friend_id: str) -> None:
        """
            Function that adds the given string id to the sent_friend_requests list
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to add to the sent_friend_requests list
            :return: None
        """
        if not friend_id in self.sent_friend_requests:
            self.sent_friend_requests.append(friend_id)
            self.save()


    def undo_fr(self, friend_id: str) -> None:
        """
            Function that cancel an already sent friend request
            :param self: Instance of the present model
            :param friend_id: String that contains the id of the user to remove from the sent_friend_requests list
            :return: None
        """
        if friend_id in self.sent_friend_requests:
            self.sent_friend_requests.remove(friend_id)
            self.save()


    def add_to_closefriends(self, new_closefriend_id: str):
        """
            Function that adds the given string id to the close_friends list if not present already
            :param self: Instance of the present model
            :param new_closefriend_id: String that contains the id of the user to add to the close_friends list
            :return: None
        """
        if not new_closefriend_id in self.close_friends:
            self.close_friends.append(new_closefriend_id)
            self.save()

    
    def remove_from_closefriends(self, ex_closefriend_id: str):
        """
            Function that removes the given string id from the close_friends list
            :param self: Instance of the present model
            :param ex_closefriend_id: String that contains the id of the user to remove from the close_friends list
            :return: None
        """
        if ex_closefriend_id in self.close_friends:
            self.close_friends.remove(ex_closefriend_id)
            self.save()

    
    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    
    


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='posts/', null=True, blank=True, default=None)
    video = models.FileField(upload_to='posts/videos', null=True, blank=True, default=None)
    description = models.TextField(max_length=280)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )
    disliked_by = ArrayField(
        models.CharField(max_length=40, blank=True, null=True),
        default=list,
        null=True,
        blank=True
    )


    def __repr__(self):
        return f"Post: {self.id} by {self.author.name} at {self.timestamp}"


    def __str__(self):
        return f"Post: {self.id} by {self.author.name} at {self.timestamp}"

    
    def has_already_liked(self, user_id: str) -> bool:
        """
            Function that checks if the given string id already exists in the liked_by list
            :param self: Instance of the present model
            :param user_id: String that contains the id of the user to check if has already liked this post
            :return: bool
        """
        return user_id in self.liked_by

    
    def has_already_disliked(self, user_id: str) -> bool:
        """
            Function that checks if the given string id already exists in the disliked_by list
            :param self: Instance of the present model
            :param user_id: String that contains the id of the user to check if has already disliked this post
            :return: bool
        """
        return user_id in self.disliked_by
    
    
    def add_like(self, liked_by: str) -> None:
        """
            Function that updates the likes count from this post
            :param self: Instance of the present model
            :param liked_by: String that contains the id of the user that has given like
            :return: None
        """
        if liked_by not in self.liked_by:
            self.liked_by.append(liked_by)
            self.likes += 1
            self.save()

    
    def remove_like(self, liked_removed_by: str) -> None:
        """
            Function that updates the likes count from this post
            :param self: Instance of the present model
            :param liked_removed_by: String that contains the id of the user that has no longer liked the post
            :return: None
        """
        if self.likes > 0:
            self.liked_by.remove(liked_removed_by)
            self.likes -= 1
            self.save()


    def add_dislike(self, disliked_by: str) -> None:
        """
            Function that updates the dislikes count from this post
            :param self: Instance of the present model
            :param disliked_by: String that contains the id of the user has given dislike
            :return: None
        """
        if disliked_by not in self.disliked_by:
            self.disliked_by.append(disliked_by)
            self.dislikes += 1
            self.save()


    def remove_dislike(self, dislike_removed_by: str) -> None:
        """
            Function that updates the dislikes count from this post
            :param self: Instance of the present model
            :param dislike_removed_by: String that contains the id of the user that has no longer disliked the post
            :return: None
        """
        if self.dislikes > 0:
            self.disliked_by.remove(dislike_removed_by)
            self.dislikes -= 1
            self.save()
        

    def get_comments(self):
        """
            Function that gets all the Comment objects related to this post
            :param self: Instance of the present model
            :return: QuerySet
        """
        return self.comments_set.all()


    class Meta:
        ordering = ["-timestamp"]


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    # name = models.CharField(max_length=180, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.content} by: {self.sender} to: {self.recipient}"


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=280)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __repr__(self) -> str:
        return f"Comment by: {self.author.name} at {self.timestamp}"

    
    def __str__(self) -> str:
        return f"Comment by: {self.author.name} at {self.timestamp}"


    class Meta:
        ordering = ['-timestamp']
