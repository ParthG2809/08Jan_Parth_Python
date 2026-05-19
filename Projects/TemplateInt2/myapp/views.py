from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cheackout(request):
    return render(request, 'cheackout.html')

def contact(request):
    return render(request, 'contact.html')

def cart(request):
    return render(request, 'cart.html')

def shop(request):
    return render(request, 'shop.html')