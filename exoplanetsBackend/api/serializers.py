from rest_framework import serializers
from .models import ChatMessage, Conversation, Exoplaneta

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Conversation
        fields= '__all__'

class ExoplanetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exoplaneta
        fields = '__all__'

class ExoplanetaQuizSerializer(serializers.Serializer):
    exoplaneta_id = serializers.IntegerField()
    respuestas = serializers.ListField(child=serializers.CharField())