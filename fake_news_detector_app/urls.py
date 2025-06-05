from django.urls import path
from .views import SignUpView, MyTokenObtainPairView, NewsDetectionView, DetectionHistoryView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detect/', NewsDetectionView.as_view(), name='detect'),
    path('history/', DetectionHistoryView.as_view(), name='history')
]


