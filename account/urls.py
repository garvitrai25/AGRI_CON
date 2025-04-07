from django.urls import include, path

from .views import editUserInfo, login_view, signup, user_logout, user_profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('userprofile/', user_profile, name='userprofile'),
    path('editUserInfo/', editUserInfo, name='editUserInfo'),
    path('', include('django.contrib.auth.urls')),
]
