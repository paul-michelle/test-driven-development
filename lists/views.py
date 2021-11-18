from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from .models import Item, List


def home_page(request):
    return render(request, 'lists/home.html')


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error_message = mark_safe("Please fill in the form. It can't be empty")
        return render(request, 'lists/home.html', {'error': error_message})
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'list': list_})


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
