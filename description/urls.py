from django.urls import path
from .views import GenerateDescriptionAPIView

urlpatterns = [
    path('generate-description/', GenerateDescriptionAPIView.as_view(), name='generate-description'),
]
