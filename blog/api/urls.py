from django.urls import path
from . import views

urlpatterns = [ 
    path("profiles/", views.get_profiles),
    path("friends/add_fr/<str:fr_sent_by>/<str:fr_sent_to>/", views.add_friend_request),
    path("friends/undo_fr/<str:curr_user_username>/<str:fr_to_remove_username>/", views.undo_friend_request),
    path("friends/accept_fr/<str:curr_user_username>/<str:new_friend>/", views.add_friend),
    path("friends/delete_fr/<str:curr_user_username>/<str:fr_username_to_delete>/", views.delete_friend_request),
    path("friends/remove_friend/<str:curr_user_username>/<str:friend_to_remove_username>/", views.remove_friend),

    path("friends/add_to_cf/<str:curr_user_username>/<str:new_closefriend_username>/", views.add_friend_to_closefriends),
    path("friends/remove_from_cf/<str:curr_user_username>/<str:ex_closefriend_username>/", views.remove_friend_from_closefriends),


    path("posts/", views.get_posts),
    path("posts/addlike/<str:post_id>/<str:liked_by>/", views.add_like),
    path("posts/remove_like/<str:post_id>/<str:like_removed_by>/", views.remove_like),
    path("posts/comment/<str:post_id>/<str:commented_by_id>/", views.add_comment),
    path("posts/add_dislike/<str:post_id>/<str:disliked_by>/", views.add_dislike),
    path("posts/remove_dislike/<str:post_id>/<str:dislike_removed_by>/", views.remove_dislike),
]