from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'password-reset-tokens', views.PasswordResetTokenViewSet)
router.register(r'diet-food-list', views.DietFoodListViewSet)
router.register(r'diets', views.DietViewSet)
router.register(r'period-with-food-list', views.PeriodWithFoodListViewSet)
router.register(r'fees', views.FeesViewSet)
router.register(r'exercise-list', views.ExerciseListViewSet)
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'workouts', views.WorkOutViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'attendance', views.AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Basit giriş endpoint'i
    path('auth/login/', views.simple_login, name='simple-login'),
] 