from rest_framework import generics
from rest_framework.response import Response

from landing.models import *
from .serializers import *

# Create your views here.

class FaqListView(generics.ListAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer

class FaqView(generics.GenericAPIView):
    serializer_class = FaqSerializer