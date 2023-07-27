from rest_framework import serializers
from .models import User, Question

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    # Add a custom field 'status' to the serializer
    status = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question', 'option1', 'option2', 'option3', 'option4', 'option5', 'answer', 'explain', 'status']

    def get_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check if the question is read by the current user
            if request.user.readquestion_set.filter(question_id=obj.id).exists():
                return 'read'

            # Check if the question is marked as favorite by the current user
            if request.user.favoritequestion_set.filter(question_id=obj.id).exists():
                return 'favorite'

        return 'unread'
