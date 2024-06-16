from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.settings import api_settings 
from .models import User
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    
)

from rest_framework import status,viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes 
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render 
from django.views import View
from django.db.models import Q 
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy 

from django.shortcuts import render,get_object_or_404

# Create your views here.

class CreateUserView(generics.CreateAPIView):

   
    '''
    Create a new user in the system
    '''
    print("here in view")
    serializer_class = UserSerializer
    

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         print('Data is not valid')
    #         print(serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class FollowersView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self,request):
        user = request.user
        data = request.data
        user_to_follow = get_object_or_404(User,pk = data['user_pk'])
        user.follow(user_to_follow)
        return Response({'status':'following'})
    
    def get(self,request):
        user = request.user
        followers = UserSerializer(user.followers.all(),many=True)
        return Response(followers.data)

class FollowingListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request):
        user = request.user
        followers = UserSerializer(user.following.all(),many=True)
        return Response(followers.data)
    

class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a user
    '''

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user 
        return user 
    


class CreateTokenView(ObtainAuthToken):
    '''
    Create a new auth token for user
    '''

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES 

    




class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                "detail":"Password reset email has been sent. ",
            }
        )
    


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def get(self,request,uidb64,token):
        try: 
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk = uid)
        except(TypeError,ValueError,OverflowError,get_user_model().DoesNotExist):
            user = None 

        if user is not None and PasswordResetTokenGenerator().check_token(user,token):
            context = {"uidb64":uidb64,"token":token}
            return render(request,"password_rest_confirm.html",context)
        else:
            return HttpResponseBadRequest("Invalid reset link.")
        
    def post(self,request,uidb64,token):
        try: 
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk = uid)
        except(TypeError,ValueError,OverflowError,get_user_model().DoesNotExist):
            user = None 

        if user is not None and PasswordResetTokenGenerator().check_token(user,token):
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            password = serializer.validated_data["password"]
            user.set_password(password)
            user.save()

            return HttpResponseRedirect(reverse("password_reset_complete"))
        else: 
            return HttpResponseBadRequest("Invalid reset link.")
        


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context [
            "message"
        ] = "Your password has been successfully reset.Please login with your new password."
        return context 
    
    

class ListUserView(generics.ListAPIView):
    '''
    Search users by name or email. A single string will be searched in both name and email. Pass the string in search query parameter. 
    '''

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.exclude(pk = self.request.user.pk)
        search = self.request.query_params.get("search",None)
        if search is not None:
            queryset = queryset.filter(
                Q(name__icontains = search) | Q(email__icontains=search)
            )
        return queryset 
    


# 
# class CreateFollowingFollower(generics.CreateAPIView):
