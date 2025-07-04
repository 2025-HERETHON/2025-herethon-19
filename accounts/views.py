from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer

# Create your views here.
class SignupView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer