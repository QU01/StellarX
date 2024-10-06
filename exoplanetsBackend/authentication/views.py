from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso a todos los usuarios
@authentication_classes([TokenAuthentication])  # Usar autenticación por token
def auth(request, format=None):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Invalid Format", safe=False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso a todos los usuarios
def registrar_usuario(request):
    data = JSONParser().parse(request)
    serializer = UserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)