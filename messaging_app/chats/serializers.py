"""This model handles serialiizers for the models."""
from rest_framework import serializers

from .models import Conversation, CustomUser, Message


class CustomUserSerializer(serializers.modelSerializer):
    """Serializer for the CustomUser model."""

    class Meta:
        """Show meta fields."""

        model = CustomUser
        fields = (
            'id', 'user_id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'created_at'
        )
        read_only_fields = ('id', 'user_id', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Includes read-only fields for sender username and conversation ID.
    """

    sender_username = serializers.CharField(source='sender.username')
    conversation_id = serializers.CharField(
        source='conversation.conversation_id')

    class Meta:
        """Show meta fields."""

        model = Message
        fields = (
            'message_id', 'sender', 'sender_username', 'conversation',
            'conversation_id', 'message_body', 'sent_at'
        )
        read_only_fields = ('message_id', 'sent_at')
        extra_kwargs = {
            'sender': {'write_only': True},
            'conversation': {'write_only': True}
        }


class ConversationSerialzer(serializers.ModelSerializer):
    """
    Serialzer for the Conversation model.

    Includes nested MessageSerializer to show messages within a conversation.
    Also includes a list of participant usernames.
    """

    messages = MessageSerializer(many=True, read_only=True)

    participants_usernames = serializers.SerializerMethodField()

    class Meta:
        """Show meta fields."""

        model = Conversation
        fields = (
            'conversation_id', 'participants', 'participants_usernames',
            'created_at', 'messages'
        )
        read_only_fields = ('conversation_id', 'created_at', 'messages')

    def get_participants_usernames(self, obj):
        """Return a list of usernames for all participants."""
        return [user.username for user in obj.participants.all()]

    def validate_participants(self, value):
        """
        Validate a conversation has at least two participants.

        This demonstrates the use of serializers.ValidationError.
        """
        if not value:
            raise serializers.ValidationError(
                "A conversation must have at least one participant."
            )
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants."
            )
        return value
