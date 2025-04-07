from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError, send_mail
from django.db.models.signals import post_save
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from account.models import User_info, create_user_profile
from agro.models import BeatItem, Notification, Order, ProductItem

from .forms import CustomUserCreationForm, UserFLEname, UserInfo


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"✅ Welcome back, {user.get_full_name() or user.username}!")
                return redirect('home')
            else:
                # Check if user exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "❌ Incorrect password. Please try again.")
                else:
                    messages.error(request, "❌ User does not exist. Please check your username or sign up.")
                    
        return render(request, 'account/login.html')
    else:
        return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "✅ Registration successful! Please login with your credentials.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='/account/login/')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        if cart := request.session.get('cart'):
            cart = {}
        return redirect('login')
    else:
        return redirect('login')


@login_required(login_url='/account/login/')
def user_profile(request):
    user = request.user
    
    # Try to get user_profile, create if it doesn't exist
    try:
        user_profile = User_info.objects.get(user=user)
    except User_info.DoesNotExist:
        # Create a default User_info for the user
        user_profile = User_info(
            user=user,
            gender='M',  # Default value
            address='Your Address',  # Default value
            phone='Your Phone Number',  # Default value
            user_type='B',  # Default as Buyer
            profile_pic='profilepic/default.jpg'  # Using default profile pic
        )
        user_profile.save()
        messages.info(request, "We've created a default profile for you. Please update your information.")
    
    products = ProductItem.objects.filter(user=user)
    
    # Get messages sent by user
    sent_messages = BeatItem.objects.filter(user=user)
    
    # Get messages received on user's products
    received_messages = BeatItem.objects.filter(product__user=user)
    
    # Get recent orders (as buyer)
    recent_orders = Order.objects.filter(user=user).order_by('-create_date')[:5]
    
    # Get orders received as seller
    seller_orders = Order.objects.filter(seller=user).order_by('-create_date')[:10]
    
    # Get unread notifications
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-create_date')[:10]
    
    context = {
        'user': user,
        'profile': user_profile,
        'products': products,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'recent_orders': recent_orders,
        'seller_orders': seller_orders,
        'notifications': notifications
    }
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='/account/login/')
def editUserInfo(request):
    user = User.objects.get(username=request.user.username)
    
    # Try to get user_profile, create if it doesn't exist
    try:
        mydata = User_info.objects.get(user=request.user)
    except User_info.DoesNotExist:
        # Create a default User_info for the user
        mydata = User_info(
            user=request.user,
            gender='M',  # Default value
            address='Your Address',  # Default value
            phone='Your Phone Number',  # Default value
            user_type='B',  # Default as Buyer
            profile_pic='profilepic/default.jpg'  # Using default profile pic
        )
        mydata.save()
        messages.info(request, "We've created a default profile for you. Please update your information.")
    
    if request.method == 'POST':
        # Make sure to use request.FILES for file uploads
        form = UserInfo(request.POST, request.FILES, instance=mydata)
        form1 = UserFLEname(request.POST, instance=user)
        
        if form.is_valid() and form1.is_valid():
            # Debug information
            print(f"Form data: {form.cleaned_data}")
            print(f"Form1 data: {form1.cleaned_data}")
            
            # Save the forms
            form.save()
            form1.save()
            
            messages.success(request, "Profile updated successfully!")
        else:
            # If forms are not valid, show error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            
            for field, errors in form1.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
        
        return redirect('userprofile')
    else:
        form = UserInfo(instance=mydata)
        form1 = UserFLEname(instance=user)
    
    context={
        'form': form,
        'form1': form1,
        'userinfo': mydata,
    }
    return render(request, 'account/editinfo.html', context)




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')