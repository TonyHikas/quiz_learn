from rest_framework import serializers

from quiz.models import Question


class GetQuestionsRequestSerializer(serializers.Serializer):
    """Serializer for GetQuestionsView query params."""

    category_id = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    questions_count = serializers.IntegerField(min_value=1, max_value=20, default=5)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for full questions data."""

    class Meta:
        model = Question
        fields = '__all__'
