from django.shortcuts import render, redirect
from .serializer import UserSerializer, ChatSerializer
from rest_framework.viewsets import ModelViewSet
from app.models import User, Chat
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.db import IntegrityError


class UserViewSet(ModelViewSet):
    queryset=User.objects.all()
    serializer_class = UserSerializer

class ChatViewSet(ModelViewSet):
    queryset=Chat.objects.all()
    serializer_class = ChatSerializer

class RegisterView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'app/registration.html')

    def post(self, request, *args, **kwargs):
        print("len:",len(request.POST.get('password')))
        try:
            user = User.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                password=make_password(request.POST.get('password')),
                date_of_birth=request.POST.get('dob'),
                contact_number=int(request.POST.get('contact-number')))

        except IntegrityError as e:
            return JsonResponse({'status_code':409, "messege":"Email already registered."})

            friends = User.objects.all().exclude(email=user.email)
            return render(request, 'app/chat.html', {'status_code':201, 'user':user, 'friends':friends})

        auth.login(request, user)
        return redirect('/app/chat', {'status_code':200})

class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'app/login.html')

    def post(self, request, *args, **kwargs):
        print(request.POST.get('email'))
        print(request.POST.get('password'))
        user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        
        if user:
            auth.login(request, user)
            return redirect('/app/chat', {'status_code':200})

        else:
            return JsonResponse({'status_code':404, "message": "Invalid email or password!"}, safe=False)

class ChatView(View):

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        print("request.user:", request.user)
        friends = User.objects.all().exclude(email=request.user)
        return render(request, 'app/chat.html',  {'status_code':200, 'friends':friends})

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        print("ChatView:request.POST:", request.POST)
        if 'message_receiver_id' in request.POST.keys():
            # chat_log = serializers.serialize('json', Chat.objects.filter(
            #     Q(sender_id=request.user.id, receiver_id=request.POST['message_receiver_id'])|
            #     Q(sender_id=request.POST['message_receiver_id'], receiver_id=request.user.id)).order_by('id'))
            chat_log=Chat.objects.filter(sender_id=request.user.id)
            print("chat-log:", chat_log)
            return JsonResponse({"chat_log":"chat_log"})

        else:
            print("else part in ChatView.")

class LogoutView(View):
    
    @method_decorator(login_required())
    def get(self, request):
        auth.logout(request)
        return redirect('/app/login', {'status_code':200})


    # def get(self, request, *args, **kwargs):
    #     # profile = get_object_or_404(Profile, pk=pk)
    #     serializer = UserSerializer
    #     return render(request, 'app/index.html', {'serializer': serializer})

    # def post(self, request, *args, **kwargs):
    #     # profile = get_object_or_404(Profile, pk=pk)
    #     serializer = UserSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return render(request,  'app/chat.html', {'serializer': serializer.errors})
    #     serializer.save()
    #     return render(request, 'app/chat.html')