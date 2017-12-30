from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id', 'created', 'updated')

    def validate_password(self, password):
        return make_password(password)
