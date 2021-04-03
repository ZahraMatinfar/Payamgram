from django import template

# from apps.post.models import Post
from apps.post.models import Post
from apps.user.models import UserFollowing, User

register = template.Library()


def find_followings(user):
    followings_obj = UserFollowing.objects.filter(user=user.id)
    followings = [u.following_user for u in followings_obj]
    return followings


@register.inclusion_tag('user/followings_posts.html')
def followings_posts(user):
    # posts = []
    # for users in user.follower.all():
    #     posts.extend(users.following_user.post_set.order_by('-published_date'))
    # posts.sort(key=lambda post: post.published_date, reverse=True)
    # return {'posts': posts}

    # followings_obj = UserFollowing.objects.filter(user=user.id)
    # followings = [u.following_user for u in followings_obj]
    followings = find_followings(user)
    posts = []
    for user in followings:
        posts.extend(user.post_set.all().order_by('-published_date'))
    posts.sort(key=lambda x: x.published_date, reverse=True)
    return {'posts': posts}


@register.inclusion_tag('user/suggestion_posts.html')
def suggestion_posts(user):
    posts = Post.objects.exclude(likes__exact=user)
    return {'posts': posts}


@register.inclusion_tag('user/suggestion_users.html')
def suggestion_users(user):
    # followings = [user.username for user in find_followings(user)]
    users = User.objects.exclude(username__in=find_followings(user))
    return {'users':users}

@register.simple_tag()
def users(letter):
    return User.objects.filter(username__istartswith=letter)

