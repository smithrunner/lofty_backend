from django.shortcuts import render
from django.views.generic import ListView
from .models import Key

from django.http.response import JsonResponse
from django.http import FileResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from dogAPI.serializers import KeySerializer
from rest_framework.decorators import api_view
import requests

from django.core.files import File
import urllib
import urllib.request
from .models import CachedImage

from imagekit import ImageSpec
from imagekit.processors import TrimBorderColor, Adjust


class ModifiedImage(ImageSpec):
    processors = [TrimBorderColor(),
                  Adjust(contrast=1.2, sharpness=1.1)
                  ]
    format = 'JPEG'
    options = {'quality': 60}

# GET api/keys : will return a list of all key:value pairs
# POST api/keys : receives a string and uses this as a the key for a new key:value
# pair. THe key will be the inputted string, the value will default to 1
@api_view(['GET','POST'])
def key_list(request):
    # GET list of keys, POST a new key
        if request.method == 'POST':
            key_data = JSONParser().parse(request)
            new_data = {'key':key_data["key"], 'value': 1}
            
            key_serializer = KeySerializer(data=new_data)
            
            if key_serializer.is_valid():
                key_serializer.save()
                return JsonResponse(key_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(key_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'GET':
            keys = Key.objects.all()

            keys_serializer = KeySerializer(keys, many=True)
            return JsonResponse(keys_serializer.data, safe=False)


# PUT api/keys/<key> : receives a key from the URL of the endpoint, looks up
# key:value pair for that key. If one is found, increase the value by 1
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


# POST api/dogs : Will use the dog.ceo endpoint (https://dog.ceo/dog-api/documentation/)
# to retreive 24 random dog images including metadata.
@api_view(['POST'])
def dog_grab(request):
    if request.method == 'POST':
        r = requests.get('https://dog.ceo/api/breeds/image/random/1', params=request.GET)
        if r.status_code == 200:
            par = r.json()
            for entry in par['message']:

                imageField = CachedImage()
                imageField.url = entry
                imageField.cache()

            return JsonResponse({'yay':'image saved'})
        return JsonResponse({'boo':'no image saved'})


# GET /api/dogs/<ID> : Receives an ID correspending to the database table
# record number for the dog image files. This method returns the orginal image,
# a modified version of that image and the original metadata. 
@api_view(['GET'])
def dog_display(request, pk):
    try:
        cachedimage = CachedImage.objects.get(pk=pk)
    except CachedImage.DoesNotExist:
        return JsonResponse({'message': 'The image with that index does not exist'}, status=status.HTTP_404_NOT_FOUND)

    print(cachedimage.photo_modified)
    #return render(request,'index.html',{'response':cachedimage})
    return JsonResponse({"original_image":str(cachedimage.photo),
                         "modified_image":str(cachedimage.photo_modified.url),
                         "meta_data":str(cachedimage.exif)})


