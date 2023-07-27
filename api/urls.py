from django.urls import path
from .views import count_favorite_read_questions, filter_questions

urlpatterns = [
    path('users/<int:user_id>/counts/', count_favorite_read_questions, name='count_favorite_read_questions'),
    path('questions/<str:status>/', filter_questions, name='filter_questions'),
]
