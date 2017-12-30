from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from users.permisions import IsOwnerOrAdmin
from users.serializers import UserSerializer

User = get_user_model()


class UserDetailAPI(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]
