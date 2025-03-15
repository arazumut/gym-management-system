from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404

from .models import (
    User, PasswordResetToken, DietFoodList, Diet, PeriodWithFoodList,
    Fees, ExerciseList, Exercise, WorkOut, Notification, Attendance
)
from .serializers import (
    UserSerializer, PasswordResetTokenSerializer, DietFoodListSerializer,
    DietSerializer, PeriodWithFoodListSerializer, FeesSerializer,
    ExerciseListSerializer, ExerciseSerializer, WorkOutSerializer,
    NotificationSerializer, AttendanceSerializer
)

# Create your views here.

# Kullanıcı görünümleri
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Liste görünümü için kimlik doğrulama gerekmez,
        diğer işlemler için kimlik doğrulama gerekir.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Şifre sıfırlama token'ları
class PasswordResetTokenViewSet(viewsets.ModelViewSet):
    queryset = PasswordResetToken.objects.all()
    serializer_class = PasswordResetTokenSerializer

# Diyet yemek listesi
class DietFoodListViewSet(viewsets.ModelViewSet):
    queryset = DietFoodList.objects.all()
    serializer_class = DietFoodListSerializer

# Diyet
class DietViewSet(viewsets.ModelViewSet):
    queryset = Diet.objects.all()
    serializer_class = DietSerializer
    
    def get_queryset(self):
        queryset = Diet.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

# Yemek periyotları
class PeriodWithFoodListViewSet(viewsets.ModelViewSet):
    queryset = PeriodWithFoodList.objects.all()
    serializer_class = PeriodWithFoodListSerializer

# Ücretler
class FeesViewSet(viewsets.ModelViewSet):
    queryset = Fees.objects.all()
    serializer_class = FeesSerializer
    
    def get_queryset(self):
        queryset = Fees.objects.all()
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email=email)
        return queryset

# Egzersiz listesi
class ExerciseListViewSet(viewsets.ModelViewSet):
    queryset = ExerciseList.objects.all()
    serializer_class = ExerciseListSerializer

# Egzersiz
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    
    def get_queryset(self):
        queryset = Exercise.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

# Antrenman
class WorkOutViewSet(viewsets.ModelViewSet):
    queryset = WorkOut.objects.all()
    serializer_class = WorkOutSerializer

# Bildirimler
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = Notification.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Yoklama
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def get_queryset(self):
        queryset = Attendance.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

# Basit giriş görünümü
@api_view(['POST'])
def simple_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'E-posta ve şifre gereklidir'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        # Şifre kontrolü
        if check_password(password, user.password):
            # Kullanıcı bilgilerini döndür
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Giriş başarılı'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Geçersiz şifre'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except User.DoesNotExist:
        return Response({'error': 'Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
