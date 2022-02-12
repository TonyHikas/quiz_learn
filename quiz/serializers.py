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
        exclude = ['question', 'right']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for get questions for quiz."""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
