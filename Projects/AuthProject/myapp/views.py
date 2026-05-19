from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import logout

# Create your views here.
def index(request):
    if request.method=='POST':
        em=request.POST["email"]
        pw=request.POST["password"]

        user=UserSignup.objects.filter(email=em, password=pw)
        if user:
            print("Login Successful!")

            request.session["user"]=em #session generate #session is stored in dictionary format    #Seesion is stored for 14 days in Django
            return redirect('home')
        else:
            print("Error! Login Failed. Please Try Again")
    return render(request, 'index.html')

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print("SignUp Successfully!")
            return redirect('/')
        else:
            print(form.errors)
    return render(request, 'signup.html')

def home(request):
    #Session get
    user=request.session.get('user')
    return render(request, 'home.html', {'user':user})

def userlogout(request):
    logout(request)
    return redirect('/')