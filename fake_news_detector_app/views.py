from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, MyTokenObtainPairSerializer, NewsDetectionSerializer
from .models import CustomUserModel, NewsDetection
from transformers import pipeline

class SignUpView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUserModel.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "New user created successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Something went wrong", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

classifier = pipeline("text-classification", model="Pulk17/Fake-News-Detection")


LABEL_MAP = {
    "LABEL_0": "REAL",
    "LABEL_1": "FAKE"
}

class NewsDetectionView(generics.GenericAPIView):
    serializer_class = NewsDetectionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Text is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        result = classifier(text)[0]
        raw_label = result['label']
        label = LABEL_MAP.get(raw_label, raw_label)
        confidence = float(result['score'])


        detection = NewsDetection.objects.create(
            user = request.user,
            text = text,
            detection = label,
            confidence = confidence
        )

        serializer = self.get_serializer(detection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DetectionHistoryView(generics.GenericAPIView):
    serializer_class = NewsDetectionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = NewsDetection.objects.filter(user=self.request.user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
