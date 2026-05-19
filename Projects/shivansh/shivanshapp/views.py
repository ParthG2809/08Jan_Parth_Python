from django.shortcuts import render, redirect
from .forms import *
from .models import shivu

# Create your views here.
def index(request):
    if request.method=="POST":
        form=studform(request.POST)
        if form.is_valid():
            form.save()
            print("Data inserted")
        else:
            print(form.error)
    return render(request,'index.html')


def showdata(request):
    data=shivu.objects.all()
    return render(request,'showdata.html',{'data': data})

def deletedata(request, id):
    obj = shivu.objects.get(id=id)
    obj.delete()
    return redirect('showdata')

def updatedata(request, id):
    obj = shivu.objects.get(id=id)
    if request.method == "POST":
        form = studform(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            print("Data updated")
            return redirect('showdata')
        else:
            print(form.error)
    return render(request, 'updatedata.html', {'obj': obj})




