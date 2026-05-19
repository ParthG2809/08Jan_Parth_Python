from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    data = response.json()
    return render(request, 'index.html', {'data': data})