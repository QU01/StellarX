from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('chat/', views.chat ),
    path('chat/delete/', views.delete_conversation),
    path('chat/get-titles', views.get_title),
    path('chat/get-data/', views.get_data),
    path('exoplaneta/preguntas/', views.generar_preguntas_exoplaneta),
    path('exoplaneta/calificar/', views.calificar_respuestas_exoplaneta),
     path('crear-exoplaneta/', views.crear_exoplaneta, name='crear_exoplaneta'),
     path('obtener-exoplanetas/', views.obtener_exoplanetas, name='obtener_exoplanetas')
]