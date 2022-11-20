from django.shortcuts import render
from django.views.generic import ListView
from .models import Key

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from dogAPI.serializers import KeySerializer
from rest_framework.decorators import api_view

class KeyListView(ListView):
    model = Key

@api_view(['GET','POST'])
def key_list(request):
    # GET list of keys, POST a new key
        if request.method == 'POST':
            key_data = JSONParser().parse(request)
            key_serializer = KeySerializer(data=key_data)
            if key_serializer.is_valid():
                key_serializer.save()
                return JsonResponse(key_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            keys = Key.objects.all()

            keys_serializer = KeySerializer(keys, many=True)
            return JsonResponse(keys_serializer.data, safe=False)


@api_view(['PUT'])
def key_detail(request, pk):
    # find key/value pair by key
    try:
        key = Key.objects.get(key=pk)
    except Key.DoesNotExist:
        return JsonResponse({'message': 'The key does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        new_data = {'key': key.key,'value': key.value + 1}
        key_serializer = KeySerializer(key, data=new_data)
        if key_serializer.is_valid():
            key_serializer.save()
            return JsonResponse(key_serializer.data)
        return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
