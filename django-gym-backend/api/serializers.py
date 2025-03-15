from rest_framework import serializers
from .models import (
    User, PasswordResetToken, DietFoodList, Diet, PeriodWithFoodList,
    Fees, ExerciseList, Exercise, WorkOut, Notification, Attendance
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'image', 
            'role', 'is_active', 'gender', 'age', 'height', 'weight', 
            'goal', 'level', 'admin', 'trainer', 'created_at', 'updated_at'
        ]
        extra_kwargs = {'password': {'write_only': True}}

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = ['id', 'token', 'reset_at', 'user', 'created_at']

class DietFoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietFoodList
        fields = ['id', 'name', 'created_at', 'updated_at']

class PeriodWithFoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodWithFoodList
        fields = [
            'id', 'diet_food_id', 'diet_food_name', 'breakfast', 
            'morning_meal', 'lunch', 'evening_snack', 'dinner', 
            'diet', 'created_at', 'updated_at'
        ]

class DietSerializer(serializers.ModelSerializer):
    period_with_food_list = PeriodWithFoodListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Diet
        fields = [
            'id', 'student', 'from_date', 'to_date', 
            'period_with_food_list', 'created_at', 'updated_at'
        ]

class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = [
            'id', 'email', 'month', 'year', 'message', 'amount', 
            'is_paid', 'transaction_id', 'payment_date', 'created_at', 'updated_at'
        ]

class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseList
        fields = ['id', 'name', 'created_at', 'updated_at']

class WorkOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOut
        fields = [
            'id', 'exercise_id_str', 'exercise_name', 'sets', 'steps', 
            'kg', 'rest', 'exercise', 'created_at', 'updated_at'
        ]

class ExerciseSerializer(serializers.ModelSerializer):
    workouts = WorkOutSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exercise
        fields = [
            'id', 'student', 'from_date', 'to_date', 
            'workouts', 'created_at', 'updated_at'
        ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_text', 'type', 'user_email', 
            'user', 'sender', 'read', 'path_name', 'created_at', 'updated_at'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id', 'from_time', 'to_time', 'is_present', 
            'date', 'student', 'created_at', 'updated_at'
        ] 