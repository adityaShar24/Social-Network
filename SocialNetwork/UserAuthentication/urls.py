from django.urls import path
from .views import UserLoginView , UserRegisterView, UserSearchView

urlpatterns = [
    path('search/', view=UserSearchView.as_view(), name='search-user'),
    path('register/', view=UserRegisterView.as_view(), name='register'),
    path('login/', view=UserLoginView.as_view(), name='login'),
]