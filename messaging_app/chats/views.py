"""Create a view set for the chat app."""
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, CustomUser, Message
from .serializers import (
    ConversationSerializer,
    CustomUserSerializer,
    MessageSerializer
)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing CustomUser instances.

    Only read operations are allowed (list, retrieve).
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Conversation instances.

    Allows listing, retrieving, creating, updating, and deleting conversations.
    Users can only see conversations they are a part of.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter conversations to only show those the current.

        authenticated user is a participant of.
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(
                participants=user
            ).distinct().order_by('-created_at')
        return Conversation.objects.none()

    def perform_create(self, serializer):
        """
        When creating a new conversation, ensure the current user is.

        automatically added as a participant.
        """
        participants_data = self.request.data.get('participants', [])

        if not participants_data:
            participants_data = []

        if (self.request.user.is_authenticated and
                self.request.user.id not in participants_data):
            participants_data.append(self.request.user.id)

        participants = CustomUser.objects.filter(id__in=participants_data)

        if not participants.exists():
            raise serializers.ValidationError(
                "A conversation must have at least one participant."
            )

        conversation = serializer.save()

        conversation.participants.set(participants)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Message instances.

    Allows listing, retrieving, creating, updating, and deleting messages.
    Users can only see messages in conversations they are a part of.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages to only show those in conversations the current.

        authenticated user is a participant of.
        """
        user = self.request.user
        if user.is_authenticated:
            user_conversations = Conversation.objects.filter(participants=user)
            return Message.objects.filter(
                conversation__in=user_conversations
            ).order_by('sent_at')
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        When creating a new message, automatically set the sender to the.

        current authenticated user and link it to the specified conversation.
        """
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            raise serializers.ValidationError(
                {
                    "conversation": "This field is required to send a message."
                }
            )

        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id
            )
        except Conversation.DoesNotExist:
            raise serializers.ValidationError(
                {"conversation": "Conversation not found."}
            )

        convo = conversation.participants.filter(
                    id=self.request.user.id).exists()

        if not convo:
            raise serializers.ValidationError(
                "You are not a participant in this conversation."
            )

        serializer.save(sender=self.request.user, conversation=conversation)
