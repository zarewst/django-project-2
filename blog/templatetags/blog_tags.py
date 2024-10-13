from django import template
from blog.models import Category


register = template.Library()

# Функция которая возвращает все катгории из модельки Категори
@register.simple_tag()
def get_categories():
    return Category.objects.all()