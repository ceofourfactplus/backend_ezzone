from xml.etree.ElementTree import tostring
import pytz
from pytz import timezone
from datetime import date, datetime
from venv import create
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .models import Login, User
from django.http import Http404
import random

from rest_framework.parsers import FormParser, MultiPartParser


class RegisterUserAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        if not User.objects.filter(username=username).exists():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                if(User.objects.all().count() == 1):
                    first_user = User.objects.all()[0]
                    first_user.is_active = True
                    first_user.is_staff = True
                    first_user.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response('Username or password is taken, choose another one', status=400)


class UserInfo(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ConfirmPass(APIView):
    def post(self, pk, request):
        user = User.objects.get(id=request.data['id'])
        if user.check_password(request.data['password']):
            return Response('password correct', status=200)
        return Response('password Incerrect', status=400)


def create_token():
    token = random.uniform(999999999999999999999999999, 0)
    if Login.objects.filter(token=token).exists():
        return create_token()
    return token


class IsActive(APIView):
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        user = self.get_object(request.data['username'])
        if user.check_password(request.data['password']):
            if user.is_active:
                token = create_token()

                login = Login.objects.create(
                    token=token,
                    user_id=user.id,
                )
                serializer = LoginSerializer(
                    login, context={"request": request})
                return Response(serializer.data, status=201)
            return Response('your account is wait for activate', status=400)
        return Response('your password is incorrect', status=400)


class UserList(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        user = User.objects.all()

        serializer = UserSerializer(
            user, context={"request": request}, many=True)
        return Response(serializer.data, status=200)


class SearchName(APIView):
    def get(self, request, qury):
        user = User.objects.filter(nick_name__contains=qury)
        serializer = UserSerializer(
            user, context={"request": request}, many=True)
        return Response(serializer.data, status=200)


class EditUser(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise 404

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ChangeStatus(APIView):

    def put(self, request, pk, status):
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.is_working = status
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Logout(APIView):
    def post(self, request, token):
        try:
            login = Login.objects.get(token=token)
            login.logout_at = datetime.now()
            print(str(login.logout_at.replace(
                tzinfo=pytz.UTC) - login.login_at))
            login.save()
            return Response('logout', status=200)
        except login.DoesNotExist:
            return Response('token not found', status=404)


class WorkHoursSelectedTime(APIView):
    def get(self, request):
        print(request.data)
        work_hours = Login.objects.filter(
            login_at__gte=request.data['start_date'])
        # for i in work_hours:

        serializer = LoginSerializer(work_hours, many=True)
        return Response(serializer.data, status=200)
        # return Response('hello',status=200)


class WorkHours(APIView):
    def get(self, request):
        work_hours = Login.objects.filter(
            login__gte=request.data['start_date'], logout__lte=request.data['end_date'])
        serializer = LoginSerializer(work_hours, many=True)
        return Response(serializer.data, status=200)
