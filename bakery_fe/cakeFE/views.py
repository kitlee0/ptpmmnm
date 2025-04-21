from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
def home(request):
    return render(request, 'cake/home.html')
def custom_login(request):
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Chuyển hướng sau khi đăng nhập thành công
        else:
            messages.error(request, "Số điện thoại hoặc mật khẩu không đúng!")

    return render(request, "cake/login.html")
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'cake/register.html', {'form': form})
def cake_list_page(request):
    return render(request, 'cake/cake_list.html')
