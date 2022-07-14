from django import template
from users.models import Post

register = template.Library()

# Custom template filter
@register.filter(name="has_liked")
def has_liked(user_id, post_id):
    post: Post = Post.objects.get(id=post_id) # OPTIMIZE, GET ONLY THE LIKED BY LIST
    return user_id in post.liked_by


@register.filter(name="has_disliked")
def has_disliked(user_id, post_id):
    post: Post = Post.objects.get(id=post_id) # OPTIMIZE, GET ONLY THE DISLIKED BY LIST
    return user_id in post.disliked_by