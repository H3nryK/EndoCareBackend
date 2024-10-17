from rest_framework import viewsets, permissions
from rest_framework.response import Response
from core.models import ChatMessage
from core.serializers import ChatMessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        message = serializer.save(user=self.request.user)
        # Here you would integrate with your chatbot service
        # For example:
        # bot_response = chatbot_service.get_response(message.content)
        # ChatMessage.objects.create(
        #     user=self.request.user,
        #     content=bot_response,
        #     is_bot=True
        # )