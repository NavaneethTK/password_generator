from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordEntry
from cryptography.fernet import Fernet
from django.conf import settings
import random
import string
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        gender = request.data.get('gender')
        password = request.data.get('password')

        if not username or not email or not password or not gender or not phone_number:
            return Response({'message': 'All fields are required'},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)


        user = User(username=username, email=email, password=make_password(password))
        user.save()

        tokens = get_tokens_for_user(user)
        return Response({'message': 'User created successfully', 'tokens': tokens}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            tokens = get_tokens_for_user(user)
            return Response({'message': 'Login successful', 'tokens': tokens}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

fernet = Fernet(settings.FERNET_KEY)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def genpass(request):
    if request.method == 'POST':
        service_name = request.data.get('service_name')
        manual_password = request.data.get('manual_password', None)

        password = manual_password if manual_password else generate_random_password()

        encrypted_password = fernet.encrypt(password.encode())

        password_entry = PasswordEntry(user=request.user, service_name=service_name, generated_password=encrypted_password.decode())
        password_entry.save()

        return Response({'message': f'Password for {service_name} saved successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_passwords(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    password_data = []
    for entry in passwords:
        decrypted_password = fernet.decrypt(entry.generated_password.encode()).decode()
        password_data.append({
            'service_name': entry.service_name,
            'generated_password': decrypted_password
        })

    return Response(password_data, status=status.HTTP_200_OK)
