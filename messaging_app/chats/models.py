"""
The model focuses on creating design for the data models.

The models are for users, messages, and conversations.
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """Custom User model extending Django's AbstractUser."""

    user_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="Unique UUID for the user"
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="User's phone number"
    )

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        help_text="Role of the user (guest, host, or admin)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for CustomUser model."""

        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Show a string representation of the CustomUser."""
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Model representing a conversation between multiple users."""

    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique UUID for conversations"
    )

    participants = models.ManyToManyField(
        CustomUser,
        related_name='conversations',
        help_text="Users involved in this conversation"
    )

    created_at = models.DateField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp when the conversation was created"
    )

    class Meta:
        """Meta class for Conversation model."""

        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        # Corrected typo: removed trailing hyphen from '-created_at-'
        ordering = ['-created_at']

    def __str__(self):
        """Show a string representation of the Conversation."""
        return (
            f"Conversation {self.conversation_id} "
            f"with {self.participants.count()} participants"
        )


class Message(models.Model):
    """Model representing a single message within a conversation."""

    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique UUID for the message"
    )

    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The user who sent this message"
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to"
    )
    message_body = models.TextField(
        help_text="The content of the message"
    )

    sent_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp when the message was sent"
    )

    class Meta:
        """Meta class for Message model."""

        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['sent_at']

    def __str__(self):
        """Show a string representation of the class."""
        return (
            f"Message {self.message_id} from {self.sender.username} "
            f"in {self.conversation.conversation_id}"
        )
