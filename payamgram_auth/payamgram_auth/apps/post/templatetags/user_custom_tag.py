from django import template

# from apps.post.models import Post
from apps.user.models import UserFollowing

register = template.Library()


@register.inclusion_tag('user/followings_posts.html')
def followings_posts(user):
    # posts = []
    # for users in user.follower.all():
    #     posts.extend(users.following_user.post_set.order_by('-published_date'))
    # posts.sort(key=lambda post: post.published_date, reverse=True)
    # return {'posts': posts}
    followings_obj = UserFollowing.objects.filter(user=user.id)
    followings = [u.following_user for u in followings_obj]
    posts = []
    for user in followings:
        posts.extend(user.post_set.all().order_by('-published_date'))
    posts.sort(key=lambda x: x.published_date, reverse=True)
    # print(posts)
    return {'posts': posts}
