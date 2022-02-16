from app.models import User, Chat
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        # name = serializers.CharField(
    #     max_length=60,
    #     required=True,
    #     style={'input_type': 'text', 'placeholder': 'Name'},
    #     label=False
    # )
    # email = serializers.CharField(
    #     required=True,
    #     style={'input_type': 'email', 'placeholder': 'Email',  'margin-top':'100px'},
    #     label=False
    # )
    # password = serializers.CharField(
    #     max_length=10,
    #     required=True,
    #     style={'input_type': 'password', 'placeholder': 'Password'},
    #     label=False
    # )
    # date_of_birth = serializers.CharField(
    #     required=True,
    #     style={'input_type': 'date', 'placeholder': 'DOB', 'onfocus':"(this.type='date')"},
    #     label=False
    # )
    # contact_number = serializers.CharField(
    #     max_length=10,
    #     required=True,
    #     style={'input_type': 'number', 'placeholder': 'Mobile No.'},
    #     label=False
    # )
    # class Meta:
    #     model = User
    #     fields = ('name', 'email', 'password', 'date_of_birth', 'contact_number')
