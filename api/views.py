from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import User, Question, FavoriteQuestion, ReadQuestion
from .serializers import UserSerializer, QuestionSerializer

# Create your views here.

@api_view(['GET'])
def count_favorite_read_questions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    favorite_count = FavoriteQuestion.objects.filter(user_id=user).count()
    read_count = ReadQuestion.objects.filter(user_id=user).count()
    return JsonResponse({'user_id': user_id, 'favorite_count': favorite_count, 'read_count': read_count, 'user': serializer.data})

@api_view(['GET'])
def filter_questions(request, status):
    # Filter questions based on the status parameter
    if status == 'read':
        questions = Question.objects.filter(readquestion__user_id=request.user.id)
    elif status == 'unread':
        questions = Question.objects.exclude(readquestion__user_id=request.user.id)
    elif status == 'favorite':
        # Filter questions by favorite status for the authenticated user
        questions = Question.objects.filter(favoritequestion__user_id=request.user.id)
    elif status == 'unfavorite':
        questions = Question.objects.exclude(favoritequestion__user_id=request.user.id)
    else:
        return Response({'error': 'Invalid status parameter.'}, status=status.HTTP_400_BAD_REQUEST)

    # Order the queryset by a unique field (e.g., 'id') for consistent pagination
    questions = questions.order_by('id')

    # Paginate the questions (100 questions per page)
    paginator = PageNumberPagination()
    paginator.page_size = 100
    page = paginator.paginate_queryset(questions, request)

    # Serialize the paginated questions and return the response
    serializer = QuestionSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)
