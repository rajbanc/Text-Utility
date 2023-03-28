from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from .forms import  EditProfileForm,ChangePasswordForm,SignUpform
from django.contrib.auth.tokens import PasswordResetTokenGenerator



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(request, username=username, password=password,email = email)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm(request.POST)
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                print("hello")
                messages.warning(request,"User is Superuser")
                return redirect('/admin')
        
            elif user.is_active:
                login(request, user)
                print("hello1")
                return redirect('/index',messages.info(request, 'You have been logged in successfully'))
            
            elif user is not authenticate:
                login(request, user)
                return redirect("registration/register.html", messages.success(request,"You must register first!"))
        
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('/login')
    
    else:
        return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)
        print(form)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/change_password.html', context)



def home(request):
    return render(request,'base.html')
def index(request):
    return render(request,'index.html')
   
def analyze(request):
    djtext = request.POST.get('text','default')
   
    
    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    capitalized = request.POST.get('capitalized','off')
    charcount = request.POST.get('charcount','off')

    #Check which checkbox is on
    if removepunc == "on":
        punctuations = '''[{!()-]};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {'purpose':'Removed Punctuations', 'analyzed_text': analyzed}
        djtext=analyzed
        
    if fullcaps =="on":
        analyzed=""
        for char in djtext:
            analyzed=analyzed+char.upper()
        params = {'purpose':'All Character are Uppercase', 'analyzed_text': analyzed}
        djtext=analyzed
    
    if(extraspaceremover=="on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext=analyzed
    
    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext:
            if char != "\n" and char!="\r":
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext=analyzed

    if (capitalized == "on"):
        analyzed = ""
        for char in djtext:
            analyzed=djtext.title()

        params = {'purpose': 'capitalized', 'analyzed_text': analyzed}
        djtext=analyzed
    
    if (charcount == "on"):
        analyzed = ""
        for char in djtext:
            analyzed=len(djtext)

        params = {'purpose': 'charcount', 'analyzed_text': analyzed}
        djtext = analyzed
    
    if(removepunc != "on" and newlineremover!="on" and extraspaceremover!="on" and fullcaps!="on" and capitalized!="on" and charcount!="on"):
        return HttpResponse("please select any operation and try again")

    return render(request, 'analyze.html', params)
