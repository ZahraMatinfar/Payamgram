from django import template

register = template.Library()


@register.filter(name='age')
def age_filter(age):
    """
    :param age: age of a post
    :return: user friendly and text age of a post
    """
    year = age.days // 365
    month = age.days // 30
    day = age.days
    hour = (age.seconds // 60) // 60

    if year == 1:
        return f'{year} year ago'
    elif year > 1:
        return f'{year} years ago'
    else:
        if month == 1:
            return f'{month} month ago'
        elif month > 1:
            return f'{month} months ago'
        else:
            if day == 1:
                return f'{day} day ago'
            elif day > 1:
                return f'{day} days ago'
            else:
                if hour == 1:
                    return f'{hour} hour ago'
                elif hour > 1:
                    return f'{hour} hours ago'
                else:
                    return 'some time ago'
