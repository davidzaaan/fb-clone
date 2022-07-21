from django.shortcuts import redirect, render
from .forms import EditProfileForm, ProfileForm, PostForm
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

# authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# error handling exceptions
from django.core.exceptions import ObjectDoesNotExist

# paginators needed
from django.core.paginator import Paginator

# utils file import
from .utils import get_registerform_data, create_new_user


def register_user(request: HttpRequest) -> None:

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            # Getting the Form instance
            profile = form.save(commit=False)

            # Getting the data coming from the form to create the new user
            data: dict = get_registerform_data(request)

            # New user creation
            user: User = create_new_user(data)

            profile.user = user
            profile.save()
            
            # Starting a new user session
            login(request, user)

            return redirect("profile", profile.id)
        else:
            if form.has_error:
                messages.error(request, form.errors.as_text())
            else:
                print(request.POST)
         
    return render(request, 'users/register.html', {})


def login_user(request: HttpRequest) -> None:

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username # OPTIMIZE
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                raise ObjectDoesNotExist("Oops, the credentials you entered doesn't match with any user")


        except ObjectDoesNotExist as err:
            messages.error(request, str(err))
            return redirect("login")

        except ValueError as ve:
            messages.error(request, str(ve))
            return redirect("login")

    else:
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, 'users/index.html', {})


@login_required
def logout_user(request: HttpRequest) -> None:
    logout(request)
    return redirect("login")


@login_required
def home(request: HttpRequest) -> None:
    if request.method == "POST":
        # Instance with the form body comming from the request object
        post_form: PostForm = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            profile: Profile = Profile.objects.get(id=request.user.profile.id) # Optimize
            
            post = post_form.save(commit=False)
            post.author = profile
            post.save()


            messages.success(request, "Post submitted successfully")

            return redirect("home")
        else:
            # If there was some corrupted or incorrect file format uploaded
            error_messages: str = post_form.errors.as_text()
            # Display the errors
            messages.error(request, error_messages)
    else:
        posts: Post = Post.objects.all() # OPTIMIZE
        current_user_id: str = str(request.user.profile.id)

        return render(request, 'users/feed.html', {
            "posts": posts,
            "current_user_id": current_user_id
        })


@login_required
def see_post(request: HttpRequest, post_id: str) -> None:
    post: Post = Post.objects.get(id=post_id) # OPTIMIZE
    current_user_id: str = str(request.user.profile.id)

    # Comments pagination options
    comment = Paginator(post.comment_set.all(), 3)
    page = request.GET.get("comment")
    comments = comment.get_page(page)

    return render(request, "users/post.html", {
        "post": post,
        "current_user_id": current_user_id,
        "comments": comments
    })


@login_required
def profile(request: HttpRequest, username: str) -> None:
    user: User = User.objects.get(username=username) # OPTIMIZE
    profile: Profile = user.profile

    return render(request, 'users/profile.html', {
        "profile": profile,
    })


@login_required
def edit_profile(request: HttpRequest) -> None:
    profile: Profile = request.user.profile
    form: EditProfileForm = EditProfileForm(instance=profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", request.user.username)

    return render(request, 'users/edit-profile.html', {
        'form': form
    })


@login_required
def my_photos(request: HttpRequest, pk: str) -> None:
    return HttpResponse("Listing photos...")