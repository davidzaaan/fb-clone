from .serializers import PostSerializer, ProfileSerializer
from users.models import Post, Comment, Profile
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import status

# http objects
from rest_framework.response import Response
from rest_framework.request import HttpRequest

# django validators
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


@api_view(['GET'])
def get_profiles(request: HttpRequest) -> Response:
    """
    Auxiliary function
    """
    profiles: Profile = Profile.objects.all() # OPTIMIZE

    serializer: ProfileSerializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_posts(request: HttpRequest) -> Response:
    """
    Auxiliary function
    """
    posts: Post = Post.objects.all()
    # print(posts)

    serializer: PostSerializer = PostSerializer(posts, many=True)
    print(serializer)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_like(request: HttpRequest, post_id: str, liked_by: str) -> Response:
    """
    Function that updates the like count from an specific post
    Args: request -> HttpRequest type object
    Returns: Response -> Response type object with the updated count of likes
    """
    try:
        post: Post = Post.objects.get(id=post_id) # OPTIMIZE TO GET ONLY THE LIKES
        user: User = User.objects.get(username=liked_by) # OPTIMIZE
    except Post.DoesNotExist:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check later
    # post: Post = get_object_or_404(Post, id=post_id)
    user_id: str = str(user.profile.id)

    post.add_like(user_id)

    if post.has_already_disliked(user_id):
        post.remove_dislike(user_id)

    return Response({
        'success': 'so far so good',
        'id': post_id,
        'likes': post.likes,
        'dislikes': post.dislikes
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def remove_like(request: HttpRequest, post_id: str, like_removed_by: str) -> Response:
    """
    Function that updates the like count from an specific post
    Args: request -> HttpRequest type object
    Returns: Response -> Response type object with the updated count of likes
    """
    try:
        post: Post = Post.objects.get(id=post_id) # OPTIMIZE TO GET ONLY THE LIKES
        user: User = User.objects.get(username=like_removed_by) # OPTIMIZE
    except Post.DoesNotExist:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user_id: str = str(user.profile.id)

    post.remove_like(user_id)

    return Response({
        'success': 'so far so good',
        'id': post_id,
        'likes': post.likes
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_dislike(request: HttpRequest, post_id: str, disliked_by: str) -> Response:
    """
    Function that updates the dislikes count from an specific post
    Args: request -> HttpRequest type object
          post_id -> str: String containing the post id to add a dislike
          disliked_by_id -> str: String containing the id of the user that disliked a post
    Returns: Response -> Response type object with the updated count of dislikes
    """
    try:
        post: Post = Post.objects.get(id=post_id) # OPTIMIZE TO GET ONLY THE DISLIKES
        user: User = User.objects.get(username=disliked_by) # OPTIMIZE
    except Post.DoesNotExist:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check later
    # post: Post = get_object_or_404(Post, id=post_id)
    user_id: str = str(user.profile.id)

    post.add_dislike(user_id)

    if post.has_already_liked(user_id):
        post.remove_like(user_id)

    return Response({
        'success': 'so far so good',
        'id': post_id,
        'dislikes': post.dislikes,
        'likes': post.likes
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def remove_dislike(request: HttpRequest, post_id: str, dislike_removed_by: str) -> Response:
    """
    Function that updates the dislikes count from an specific post
    Args: request -> HttpRequest type object
          post_id -> str: String containing the post id to add a dislike
          disliked_by_id -> str: String containing the id of the user that removed their dislike from
          a post
    Returns: Response -> Response type object with the updated count of dislikes
    """
    try:
        post: Post = Post.objects.get(id=post_id) # OPTIMIZE TO GET ONLY THE LIKES
        user: User = User.objects.get(username=dislike_removed_by) # OPTIMIZE
    except Post.DoesNotExist:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return Response({'error': 'Object does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    user_id: str = str(user.profile.id)

    post.remove_dislike(user_id)

    return Response({
        'success': 'so far so good',
        'id': post_id,
        'dislikes': post.dislikes
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_comment(request: HttpRequest, post_id: str, commented_by_id: str) -> Response:
    """
    Function that adds a comment to an specific post
    Args: request -> HttpRequest type object
          post_id -> str: String that contains the post id to the comment to be added
          commented_by_id -> str: String containing the owner of the new comment made
    Returns: Response -> Response type object with the updated count of likes
    """
    # Retrievong the data from the request's body
    comment_content = request.data
    try:
        post: Post = Post.objects.get(id=post_id) # OPTIMIZE
        commented_by: Profile = Profile.objects.get(id=commented_by_id) # OPTIMIZE
        Comment.objects.create(author=commented_by, post=post, description=comment_content)
        
        post.save()

    except Post.DoesNotExist as pdne:
        return Response({'error': str(pdne)})

    return Response({
        'success': comment_content,
        'comments_quantity': post.comment_set.all().count()
        }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_friend_request(request: HttpRequest, fr_sent_by: str, fr_sent_to: str) -> Response:
    """
    Function that adds a new friend request to both the user in session to the user selected to the request be sent
    Args: request -> HttpRequest type object
          fr_sent_by -> str: String that contains the user id from the user that made the friend request
          fr_sent_to -> str: String containing the user id to from the user that receives the friend request
    Returns: Response -> Response type object with the updated state of sent and received friend requests
    """
    sent_by: User = User.objects.get(username=fr_sent_by).profile # OPTIMIZE
    sent_to: User = User.objects.get(username=fr_sent_to).profile # OPTIMIZE

    sent_by.add_to_sent_fr(str(sent_to.id))
    sent_to.add_friend_request(str(sent_by.id))

    return Response({
        'success': 'Friend request added'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def undo_friend_request(request: HttpRequest, curr_user_username: str, fr_to_remove_username: str) -> Response:
    """
    Function that undo a friend request sent by fr_sent_by
    Args: request -> HttpRequest type object
          fr_sent_by -> str: String that contains the user id from the user that made the friend request
          fr_sent_to -> str: String containing the user id to from the user that received the friend request
    Returns: Response -> Response type object with the updated state of sent and received friend requests
    """
    sent_by: Profile = User.objects.get(username=curr_user_username).profile # OPTIMIZE
    sent_to: Profile = User.objects.get(username=fr_to_remove_username).profile # OPTIMIZE

    sent_by.undo_fr(str(sent_to.id))
    sent_to.remove_fr(str(sent_by.id))

    return Response({
        'success': 'Friend request removed'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def delete_friend_request(request: HttpRequest, curr_user_username: str, fr_username_to_delete: str) -> Response:
    """
    Function that deletes a friend request from the user object list called 'friend_requests'
    Args: request -> HttpRequest type object
          user_id -> str: String that contains the user id from the user that wants to update its friend_requests list
          fr_id_to_delete -> str: String containing the user id that the current user session wants to delete from its list
    Returns: Response -> Response type object with the updated state of the friend requests list
    """
    user: Profile = User.objects.get(username=curr_user_username).profile
    receiver: Profile = User.objects.get(username=fr_username_to_delete).profile

    user.remove_fr(str(receiver.id))
    receiver.undo_fr(str(user.id))

    return Response({
        'success': 'Friend request deleted successfully'
    }, status=status.HTTP_200_OK)



@api_view(['PATCH'])
def add_friend(request: HttpRequest, curr_user_username: str, new_friend: str) -> Response:
    """
    Function that adds a new friend request to both the user in session to the user selected to the request be sent
    Args: request -> HttpRequest type object
          fr_sent_by -> str: String that contains the user id from the user that made the friend request
          fr_sent_to -> str: String containing the user id to from the user that receives the friend request
    Returns: Response -> Response type object with the updated state of sent and received friend requests
    """
    user: Profile = User.objects.get(username=curr_user_username).profile
    new_friend: Profile = User.objects.get(username=new_friend).profile

    user.remove_fr(str(new_friend.id)) # remove the FR from the user's FR list...
    new_friend.undo_fr(str(user.id)) # undo the FR from the already made sent FR...
    user.add_friend(str(new_friend.id)) # add the new user to the current user session friends...
    new_friend.add_friend(str(user.id)) # add the current user session to the target user friends list

    return Response({
        'success': 'Friend added'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def remove_friend(request: HttpRequest, curr_user_username: str, friend_to_remove_username: str) -> Response:
    """
    Function that removes friend request to both the
    Args: request -> HttpRequest type object
          user_id -> str: String that contains the user id that wants to update its friends list
          fr_to_remove -> str: String that contains the user id to delete from the friends list of the main user
    Returns: Response -> Response type object with the updated state of sent and received friend requests
    """
    user: Profile = User.objects.get(username=curr_user_username).profile # OPTIMIZE
    ex_friend: Profile = User.objects.get(username=friend_to_remove_username).profile # OPTIMIZE

    user.remove_friend(str(ex_friend.id))
    user.remove_from_closefriends(str(ex_friend.id))

    ex_friend.remove_friend(str(user.id))
    ex_friend.remove_from_closefriends(str(user.id))

    return Response({
        'success': 'friend deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_friend_to_closefriends(request: HttpRequest, curr_user_username: str, new_closefriend_username: str) -> Response:
    """
    Function that removes friend request to both the
    Args: request -> HttpRequest type object
          user_id -> str: String that contains the user id that wants to update its close friends list
          new_closefriend_id -> str: String that contains the user id to add to the current user close friends list
    Returns: Response -> Response type object with the updated state list of the current user's close friends list
    """
    user: Profile = User.objects.get(username=curr_user_username).profile # OPTIMIZE
    new_close_friend: Profile = User.objects.get(username=new_closefriend_username).profile # OPTIMIZE

    user.add_to_closefriends(str(new_close_friend.id))

    return Response({
        'success': 'Friend added successfully to close friends'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def remove_friend_from_closefriends(request: HttpRequest, curr_user_username: str, ex_closefriend_username: str) -> Response:
    """
    Function that removes friend request to both the
    Args: request -> HttpRequest type object
          user_id -> str: String that contains the user id that wants to update its close friends list
          ex_closefriend_id -> str: String that contains the former friend id that the current user wants to remove from close_friends list
    Returns: Response -> Response type object with the updated state list of the current user's close friends list
    """
    user: Profile = User.objects.get(username=curr_user_username).profile
    ex_close_friend: Profile = User.objects.get(username=ex_closefriend_username).profile

    user.remove_from_closefriends(str(ex_close_friend.id))

    return Response({
        'success': 'Friend removed successfully from close friends'
    }, status=status.HTTP_200_OK)