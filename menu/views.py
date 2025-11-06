# menu/views.py
from django.shortcuts import render
from .models import Category


def menu_view(request):
    categories = Category.objects.prefetch_related('menuitem_set__sizes').all()
    return render(request, 'menu/menu.html', {'categories': categories})
