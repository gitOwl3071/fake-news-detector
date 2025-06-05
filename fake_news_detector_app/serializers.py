from rest_framework import serializers
from .models import CustomUserModel, NewsDetection
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = CustomUserModel
        fields = '__all__'

    def create(self, validated_data):
        return CustomUserModel.objects.create_user(email=validated_data['email'], password=validated_data['password'])
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
class NewsDetectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsDetection
        fields = '__all__'
        read_only_fields = ['detection', 'confidence', 'created_at']