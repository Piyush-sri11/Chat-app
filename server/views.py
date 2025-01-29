from django.shortcuts import render, redirect
from .models import CustomUser,ChatModel
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

@login_required(login_url="/login")
def home(request):    
    users=CustomUser.objects.exclude(email=request.user.email)

    context = {'users':users}
    print(context)
    return render(request, "index.html", context)

@login_required(login_url="/login")
def chatPage(request, username):
    try:
        user_obj = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist")


    users=CustomUser.objects.exclude(email=request.user.email)

    if request.user.id > user_obj.id:
        thread_name = f"{request.user.id}-{user_obj.id}"
    else:
        thread_name = f"{user_obj.id}-{request.user.id}"
    
    chat_messages=ChatModel.objects.filter(thread_name=thread_name)

    context = {'users':users, 'user_obj':user_obj, 'messages':chat_messages}
    print(context)
    return render(request, "chatPage.html", context=context)



def login(request):
    if(request.method == "POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(email, password)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("/login")
        
        if user.check_password(password):
            auth_login(request, user)
            print("User logged in")

            return redirect("/home")
        else:
            messages.error(request, "Invalid password.")
            print("Invalid password")
            return redirect("/login")
        # print("User not login")
    return render(request, "login.html")

def register(request):
    if(request.method == "POST"):
        email = request.POST.get("email")
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        confrim_password = request.POST.get("confirm-password")
        print(email, password, first_name, last_name)
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/register")
        if CustomUser.objects.filter(username=user_name).exists():
            messages.error(request, "Username already exists")
            return redirect("/register")
        if password != confrim_password:
            messages.error(request, "Password does not match")
            return redirect("/register")
        
        user = CustomUser(email=email, username=user_name, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return redirect("/")
    return render(request, "register.html")

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('/login')
