from django.urls import path, include
from rest_framework_nested import routers 
from .views import CustomUserViewSet, ConversationViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)

conversations_router.register(r'messages', MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
