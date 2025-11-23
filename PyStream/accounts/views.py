from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect("/")  # Redirect to homepage (we will create it soon)
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    return render(request, "accounts/login.html")

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect("signup")

        # Create new user
        user = User.objects.create_user(
            username=email.split("@")[0],   # temporary username
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "accounts/signup.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home")