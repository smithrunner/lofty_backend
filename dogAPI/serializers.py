from rest_framework import serializers
from dogAPI.models import Key

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('key','value')
