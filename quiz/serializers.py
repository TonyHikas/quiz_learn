from rest_framework import serializers

from quiz.models import Question, Answer


class GetQuestionsRequestSerializer(serializers.Serializer):
    """Serializer for GetQuestionsView query params."""

    category_id = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    questions_count = serializers.IntegerField(min_value=1, max_value=20, default=5)


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for answer data for question."""

    class Meta:
        model = Answer
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for get questions for quiz."""

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class UserAnswerSerializer(serializers.Serializer):
    """Serializer for user answers request."""

    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class UserAnswerCheckSerializer(serializers.Serializer):
    """Result of checking one user answer."""

    is_right = serializers.BooleanField()

    user_answer_id = serializers.IntegerField(required=False)
    user_answer_description = serializers.CharField(required=False, allow_blank=True)

    right_answer_id = serializers.IntegerField()
    right_answer_description = serializers.CharField(required=False, allow_blank=True)


class AnswerCheckResponseSerializer(serializers.Serializer):
    """Serializer for response for answer check."""

    right = serializers.IntegerField(min_value=0)
    total = serializers.IntegerField(min_value=0)
    check_result = UserAnswerCheckSerializer(many=True)
