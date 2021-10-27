from django.shortcuts import render, redirect
from .models import Item
# from django.http import HttpResponse

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items':items})
