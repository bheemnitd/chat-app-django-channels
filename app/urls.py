from django.urls import path, include
from .views import LoginView, RegisterView, ChatView, LogoutView
from app import views
from rest_framework import routers
from django.contrib.auth.decorators import login_required, permission_required
router = routers.DefaultRouter()
router.register('user', views.UserViewSet, basename="user")
router.register('chat', views.ChatViewSet, basename="chat")

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('registration', RegisterView.as_view(), name='registration'),
    path('chat', ChatView.as_view(), name='chat'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api', include(router.urls)),
]