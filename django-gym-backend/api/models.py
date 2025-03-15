from django.db import models
from django.contrib.auth.models import AbstractUser

# Enum seçenekleri
class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    TRAINER = 'trainer', 'Trainer'
    USER = 'user', 'User'

class Gender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'

class Goal(models.TextChoices):
    GAIN_WEIGHT = 'gain_weight', 'Gain Weight'
    LOSE_WEIGHT = 'lose_weight', 'Lose Weight'
    GET_FITTER = 'get_fitter', 'Get Fitter'
    GET_STRONGER = 'get_stronger', 'Get Stronger'
    GET_HEALTHIER = 'get_healthier', 'Get Healthier'
    GET_MORE_FLEXIBLE = 'get_more_flexible', 'Get More Flexible'
    GET_MORE_MUSCULAR = 'get_more_muscular', 'Get More Muscular'
    LEARN_THE_BASICS = 'learn_the_basics', 'Learn The Basics'

class Level(models.TextChoices):
    BEGINNER = 'beginner', 'Beginner'
    INTERMEDIATE = 'intermediate', 'Intermediate'
    ADVANCED = 'advanced', 'Advanced'
    EXPERT = 'expert', 'Expert'
    PROFESSIONAL = 'professional', 'Professional'

class Month(models.TextChoices):
    JANUARY = 'January', 'January'
    FEBRUARY = 'February', 'February'
    MARCH = 'March', 'March'
    APRIL = 'April', 'April'
    MAY = 'May', 'May'
    JUNE = 'June', 'June'
    JULY = 'July', 'July'
    AUGUST = 'August', 'August'
    SEPTEMBER = 'September', 'September'
    OCTOBER = 'October', 'October'
    NOVEMBER = 'November', 'November'
    DECEMBER = 'December', 'December'

class NotificationType(models.TextChoices):
    DIET = 'diet', 'Diet'
    EXERCISE = 'exercise', 'Exercise'
    FEES = 'fees', 'Fees'
    PAYMENT = 'payment', 'Payment'
    REMINDER = 'reminder', 'Reminder'
    MESSAGE = 'message', 'Message'
    PRESENT = 'present', 'Present'

# User modeli
class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    age = models.IntegerField(default=18)
    height = models.IntegerField(default=100)
    weight = models.IntegerField(default=50)
    goal = models.CharField(max_length=20, choices=Goal.choices, default=Goal.LOSE_WEIGHT)
    level = models.CharField(max_length=15, choices=Level.choices, default=Level.BEGINNER)
    
    admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='admins_for_users')
    trainer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='trainers_for_users')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PasswordResetToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    reset_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    created_at = models.DateTimeField(auto_now_add=True)

class DietFoodList(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Diet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diets')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PeriodWithFoodList(models.Model):
    diet_food_id = models.CharField(max_length=255)
    diet_food_name = models.CharField(max_length=255)
    breakfast = models.BooleanField(default=False)
    morning_meal = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    evening_snack = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name='period_with_food_list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Fees(models.Model):
    email = models.EmailField()
    month = models.CharField(max_length=15, choices=Month.choices)
    year = models.CharField(max_length=4)
    message = models.TextField()
    amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ExerciseList(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exercise(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkOut(models.Model):
    exercise_id_str = models.CharField(max_length=255)
    exercise_name = models.CharField(max_length=255)
    sets = models.IntegerField()
    steps = models.IntegerField()
    kg = models.IntegerField()
    rest = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workouts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    notification_text = models.TextField()
    type = models.CharField(max_length=15, choices=NotificationType.choices)
    user_email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent', null=True, blank=True)
    read = models.BooleanField(default=False)
    path_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    from_time = models.CharField(max_length=10)
    to_time = models.CharField(max_length=10)
    is_present = models.BooleanField(default=False)
    date = models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
