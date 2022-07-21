from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [ 
    path('', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('home/', views.home, name="home"),
    path('post/<str:post_id>/', views.see_post, name="see_post"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('photos/<str:pk>/', views.my_photos, name="my_photos"),

    # Forgot password handling
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='password-reset-1.html'), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password-reset-2.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-3.html'), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-4.html'), name="password_reset_complete"),
]
