from django import template
from users.models import Post
from django.contrib.auth.models import User

register = template.Library()

# Custom template filter
@register.filter(name="has_liked")
def has_liked(username, post_id):
    post: Post = Post.objects.get(id=post_id) # OPTIMIZE, GET ONLY THE LIKED BY LIST

    user: User = User.objects.get(username=username) # OPTIMZE
    user_id: str = str(user.profile.id)

    return user_id in post.liked_by


@register.filter(name="has_disliked")
def has_disliked(username, post_id):
    post: Post = Post.objects.get(id=post_id) # OPTIMIZE, GET ONLY THE DISLIKED BY LIST

    user: User = User.objects.get(username=username) # OPTIMZE
    user_id: str = str(user.profile.id)
    
    return user_id in post.disliked_by