from rest_framework import serializers
from app.newblogapp.models import Account
from app.newblogapp.jwt_helper import get_json_web_token


class SignupSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(allow_blank=False, write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name',)
        write_only_fields = ('password',)

    def validate(self, data):
        flag=0
        for k, v in data.items():
            if v == '':
                flag=1
                break
        if flag==1:
            raise serializers.ValidationError("Some fields are missing")

        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    """
        Account Signup serializer to handle user registration.
    """
    token = serializers.SerializerMethodField('get_json_web_token')

    class Meta:
        model = Account
        fields = ('token',)

    def get_json_web_token(self, obj):
        """
            Returns json web token for the user object
        """
        return get_json_web_token(obj)
