from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = { "password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)




class AuthTokenSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")


        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials", code="authorization")

        attrs["user"] = user
        return attrs



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        return token

    def validate(self, attrs):
        """Permettre l'auth via email par username"""
        attrs["username"] = attrs.get("email")
        data = super().validate(attrs)
        # Ajouter des données custom dans la réponse
        data['email'] = self.user.email
        data['name'] = self.user.name

        return data
