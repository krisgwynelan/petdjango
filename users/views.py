from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        print("Received data:", data)  # Debug log

        required_fields = ['first_name', 'last_name', 'email', 'password', 'username']
        for field in required_fields:
            if not data.get(field):
                return Response({"message": f"{field} is required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if User.objects.filter(email=data['email']).exists():
                return Response({"message": "Email is already registered!"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=data['username']).exists():
                return Response({"message": "Username is already taken!"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['username']
            )
            user.set_password(data['password'])
            user.save()

            # Generate token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"message": "User created successfully!", "token": token.key}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
