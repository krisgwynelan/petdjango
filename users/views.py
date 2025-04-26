from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        
        print("Received data:", data)  # Add a print statement to log the data

        # Validate the required fields
        required_fields = ['first_name', 'last_name', 'email', 'password', 'username']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({"message": f"{field} is required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the email is already taken
            if User.objects.filter(email=data['email']).exists():
                return Response({"message": "Email is already registered!"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the username is already taken
            if User.objects.filter(username=data['username']).exists():
                return Response({"message": "Username is already taken!"}, status=status.HTTP_400_BAD_REQUEST)

            # Create user and hash the password
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['username'],  # Make sure username is included
            )
            user.set_password(data['password'])  # Hash the password before saving
            user.save()

            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
