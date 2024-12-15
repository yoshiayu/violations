from rest_framework import serializers
from .models import User, Violations, ViolationSelection, Result

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ViolationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violations
        fields = '__all__'

class ViolationSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationSelection
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'