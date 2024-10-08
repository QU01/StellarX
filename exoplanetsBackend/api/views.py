# Create your views here.
import requests
from .serializers import ChatMessageSerializer, ConversationSerializer, ExoplanetaSerializer, ExoplanetaQuizSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import ChatMessage, Conversation, Exoplaneta
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import OpenAI
import json
from rest_framework import status
from rest_framework.response import Response

def clean_model_response(response):
    # Extract the JSON content between <start json> and <end json> tags
    json_content = response.split('<start json>')[1].split('<end json>')[0].strip()
    
    # Parse the JSON content
    cleaned_data = json.loads(json_content)
    
    return cleaned_data



llm = OpenAI(max_tokens=-1,api_key='')

memory = ConversationBufferMemory()

# API for title generator
API_URL = "https://api-inference.huggingface.co/models/czearing/article-title-generator"
headers = {"Authorization": f"Bearer YOUR_API_TOKEN"}

def generate_title(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']


# retriving the last 4 conversations from the db for memory eficiency while providing context to model
def retrieve_conversation(title, user):
    # number of conversations
    num_recent_conversations = 4

    # Retrieve the most recent conversation history from the database
    conversation_obj = Conversation.objects.get(title=title, user=user)
    conversation_id = getattr(conversation_obj, 'id')
    
    # Retrieve recent conversation messages
    conversation_context = ChatMessage.objects.filter(
        conversation_id=conversation_id
    ).order_by('-timestamp')[:num_recent_conversations:-1]
    
    # Storing the retrived data from db to model memory 
    lst = []
    for msg in conversation_context:
        input_msg = getattr(msg, 'user_response')
        output_msg = getattr(msg, 'ai_response')
        lst.append({"input": input_msg, "output": output_msg})
    
    for x in lst:
        inputs = {"input": x["input"]}
        outputs = {"output": x["output"]}
        memory.save_context(inputs, outputs)
    
   
    retrieved_chat_history = ChatMessageHistory(
        messages=memory.chat_memory.messages
    )

    return retrieved_chat_history


# Function to store the conversation to DB
def store_message(user_response, ai_response, conversation_id):
    ChatMessage.objects.create(
        user_response=user_response,
        ai_response=ai_response,
        conversation_id=conversation_id,
    )

# Function to create a Conversation in DB
def store_title(title, user):
    Conversation.objects.create(
        title=title,
        user=user
    )

# Function to Get all Chat history of conversation and create a new chat
@csrf_exempt
@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat(request):
    #get chat history
    if request.method == 'GET':
        request_data = JSONParser().parse(request)
        provided_title = request_data.get('title')
        user = request.user
        if provided_title:
            conversation_title = Conversation.objects.get(
                title=provided_title, user=user)
            conversation_id = getattr(conversation_title, 'id')
            ChatObj = ChatMessage.objects.filter(
                conversation_id=conversation_id).order_by('timestamp')
            Chat = ChatMessageSerializer(ChatObj, many=True)
            return JsonResponse(Chat.data, safe=False)
        else:
            return JsonResponse({'error': 'Title not provided'}, status=400)

    #create new chat or continue old conversation by providing title
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        prompt = request_data.get('prompt')
        user = request.user
        provided_title = request_data.get('title')
        if provided_title:
            # Create a ChatMessageHistory instance
            retrieved_chat_history = retrieve_conversation(
                provided_title, user)

        else:
            memory.clear()
            retrieved_chat_history = ChatMessageHistory(messages=[])
            # Generate a default title if not provided
            title = generate_title({
                "inputs": response
            })
            store_title(title, user)
        reloaded_chain = ConversationChain(
            llm=llm,
            memory=ConversationBufferMemory(
                chat_memory=retrieved_chat_history),
            verbose=True
        )

        response = reloaded_chain.predict(input=prompt)

        conversation_title = Conversation.objects.get(title=title, user=user)
        conversation_id = getattr(conversation_title, 'id')
        store_message(prompt, response, conversation_id)

        return JsonResponse({
            'ai_responce': response,
            'title':title
        }, status=201)



# Retriving all conversations of a user ( Titles only )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def get_title(request):
    user=request.user
    titles= Conversation.objects.filter(user=user)
    serialized= ConversationSerializer(titles, many=True)
    return JsonResponse(serialized.data, safe=False)

# Delete a conversation by providing title of conversation
@csrf_exempt   
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def delete_conversation(request):
    user=request.user
    data= JSONParser().parse(request)
    title= data.get('title')
    obj=Conversation.objects.get(user=user, title=title)
    obj.delete()
    return JsonResponse("Deleted succesfully", safe=False)

@csrf_exempt   
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    request_data = JSONParser().parse(request)
    provided_title = request_data.get('title')
    user = request.user
    if provided_title:
        conversation_title = Conversation.objects.get(
            title=provided_title, user=user)
        conversation_id = getattr(conversation_title, 'id')
        ChatObj = ChatMessage.objects.filter(
            conversation_id=conversation_id).order_by('timestamp')
        Chat = ChatMessageSerializer(ChatObj, many=True)
        return JsonResponse(Chat.data, safe=False)
    else:
        return JsonResponse({'error': 'Title not provided'}, status=400)

@csrf_exempt
@api_view(['POST'])
def generar_preguntas_exoplaneta(request):
    data = JSONParser().parse(request)
    exoplaneta_id = data.get('exoplaneta_id')

    print("exoplaneta_id")
    
    try:
        exoplaneta = Exoplaneta.objects.get(id=exoplaneta_id)
    except Exoplaneta.DoesNotExist:
        return JsonResponse({'error': 'Exoplaneta no encontrado'}, status=404)
    
    serializer = ExoplanetaSerializer(exoplaneta)
    exoplaneta_data = serializer.data
    
    prompt = f"""Genera 5 preguntas sobre el siguiente exoplaneta:\n{exoplaneta_data}\nLas preguntas deben ser variadas y cubrir diferentes aspectos del exoplaneta. Estan enfocadas a un publico joven desde preparatoria a universidad. Coloca las respuestas en formato JSON:
    
            <start json>
            {{
                "pregunta 1": {{
                    "pregunta": "",
                    "opciones": ["", "", "", ""],
                    "respuesta": ""
                }},
                "pregunta 2": {{
                    "pregunta": "",
                    "opciones": ["", "", "", ""],
                    "respuesta": ""
                }}
            }}
            <end json>
    """
    
    
    response = llm.invoke(input=prompt)

    # In your generar_preguntas_exoplaneta function, replace the return statement with:
    #cleaned_response = clean_model_response(response)
    return JsonResponse({'preguntas': response}, status=200)


@csrf_exempt
@api_view(['POST'])
def calificar_respuestas_exoplaneta(request):
    serializer = ExoplanetaQuizSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    
    exoplaneta_id = serializer.validated_data['exoplaneta_id']
    respuestas = serializer.validated_data['respuestas']
    
    try:
        exoplaneta = Exoplaneta.objects.get(id=exoplaneta_id)
    except Exoplaneta.DoesNotExist:
        return JsonResponse({'error': 'Exoplaneta no encontrado'}, status=404)
    
    serializer = ExoplanetaSerializer(exoplaneta)
    exoplaneta_data = serializer.data
    
    prompt = f"""Dado el siguiente exoplaneta:\n{exoplaneta_data}\n\nCalifica las siguientes respuestas del usuario y proporciona un puntaje final sobre 100. Devuelve la respuesta en formato JSON:

    <start json>
    {{
        "calificaciones": [
            {{
                "respuesta": "Respuesta 1",
                "puntuacion": 0,
                "explicacion": ""
            }},
            {{
                "respuesta": "Respuesta 2",
                "puntuacion": 0,
                "explicacion": ""
            }}
        ],
        "puntaje_final": 0,
        "comentario_general": ""
    }}
    <end json>

    Respuestas del usuario:
    """
    
    for i, respuesta in enumerate(respuestas, 1):
        prompt += f"\nRespuesta {i}: {respuesta}"
    
    response = llm.invoke(input=prompt)
    
    cleaned_response = clean_model_response(response)
    return JsonResponse({'calificacion': cleaned_response}, status=200)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crear_exoplaneta(request):
    # Modificado para aceptar una lista de JSON
    data = JSONParser().parse(request)
    if isinstance(data, list):
        # Guardar múltiples exoplanetas
        for item in data:
            serializer = ExoplanetaSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Exoplanetas creados exitosamente"}, status=status.HTTP_201_CREATED)
    else:
        # Manejo de error si no es una lista
        serializer = ExoplanetaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Nueva función para obtener exoplanetas
@csrf_exempt
@api_view(['GET'])
def obtener_exoplanetas(request):
    exoplaneta_id = request.query_params.get('id', None)
    if exoplaneta_id:
        try:
            exoplaneta = Exoplaneta.objects.get(id=exoplaneta_id)
            serializer = ExoplanetaSerializer(exoplaneta)
            return JsonResponse(serializer.data, status=200)
        except Exoplaneta.DoesNotExist:
            return JsonResponse({'error': 'Exoplaneta no encontrado'}, status=404)
    else:
        # Obtener todos los exoplanetas si no se proporciona un ID
        exoplanetas = Exoplaneta.objects.all()
        serializer = ExoplanetaSerializer(exoplanetas, many=True)
        return JsonResponse(serializer.data, safe=False)