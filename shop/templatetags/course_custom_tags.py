from django import template
register = template.Library()
from shop.models import UserProduct

@register.simple_tag
def is_enrolled(request,product):
    is_enrolled = False
    user = None
    if not request.user.is_authenticated:
        return False
    user = request.user
    try:
        user_course = UserProduct.objects.get(user=user,product=product)
        return True
    except:
        return False