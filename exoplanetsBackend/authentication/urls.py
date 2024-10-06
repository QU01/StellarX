#path authentication/url
from rest_framework.authtoken import views
from django.urls import path
from .views import auth, registrar_usuario
urlpatterns = [
    path('get-auth/', views.obtain_auth_token),
    path('register/', auth ),
    path('sign-in/', registrar_usuario)
]