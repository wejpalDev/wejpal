from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    prompt = serializers.CharField()



