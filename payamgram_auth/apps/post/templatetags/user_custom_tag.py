from django import template
from apps.post.models import Post
from apps.user.models import UserFollowing, User

register = template.Library()


def find_followings(user):
    """
    find users with id
    """
    followings_obj = UserFollowing.objects.filter(user=user.id)
    followings = [u.following_user for u in followings_obj]
    return followings


@register.inclusion_tag('user/followings_posts.html')
def followings_posts(user):
    """
    The posts of the people user has followed are shown
    """
    followings = find_followings(user)
    posts = []
    for user in followings:
        posts.extend(user.post_set.all().order_by('-published_date'))
    posts.sort(key=lambda x: x.published_date, reverse=True)
    return {'posts': posts}


@register.inclusion_tag('user/suggestion_posts.html')
def suggestion_posts(user):
    """
    Posts that the user has not liked yet will be notified to her
    """
    posts = Post.objects.exclude(likes__exact=user)
    return {'posts': posts}


@register.inclusion_tag('user/suggestion_users.html')
def suggestion_users(user):
    """
    Indicates people who have not yet followed
    """
    users = User.objects.exclude(username__in=find_followings(user))
    return {'users': users}


@register.simple_tag()
def users(letter):
    """
    find users with their username that start with letter that user has entered
    """
    return User.objects.filter(username__istartswith=letter)
