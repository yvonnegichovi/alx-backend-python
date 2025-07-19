from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet, ConversationViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
