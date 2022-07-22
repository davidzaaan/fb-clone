from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('', views.friends, name="friends"),
    path('requests/', views.friend_requests, name="friend-requests"),
    path('sent-requests/', views.sent_friend_requests, name="sent-friend-requests"),
    path('suggestions/', views.friend_suggestions, name="friend-suggestions"),
    path('list/<str:user_username>/', views.friends_all, name="all-friends"),
    path('birthdays/', views.friends_birthdays, name="friends-birthdays"),
    path('close-friends/', views.close_friends, name="close-friends"),
]

# for production purposes...
