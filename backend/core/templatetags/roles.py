import os

from django import template

from core.roles import can

register = template.Library()


@register.simple_tag(takes_context=True)
def user_can(context, url_name):
    request = context.get('request')
    user = getattr(request, 'user', None)
    return can(user, url_name)


@register.simple_tag
def role_label(role):
    from core.models import User
    for value, label in User.ROLE_CHOICES:
        if value == role:
            return str(label)
    return str(role)