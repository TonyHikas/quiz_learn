from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.api.docs import GetQuestionsParameters
from quiz.models import Question
from quiz.serializers import GetQuestionsRequestSerializer, QuestionSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_id='Получение списка вопросов для теста',
        responses={
            status.HTTP_200_OK: QuestionSerializer(many=True)
        },
        manual_parameters=GetQuestionsParameters
    )
)
class GetQuestionsView(GenericAPIView):
    """Get questions set for one quiz."""
    queryset = Question.objects.all()

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request, *args, **kwargs):
        request_params = GetQuestionsRequestSerializer(data=request.query_params)
        if not request_params.is_valid():
            return Response(request_params.errors, status=status.HTTP_400_BAD_REQUEST)
        request_data = request_params.validated_data

        queryset = self.get_queryset()

        if category_id := request_data.get('category_id'):
            queryset = queryset.filter(category_id=category_id)

        queryset = queryset[:request_data.get('questions_count')]
        serialized_questions = QuestionSerializer(queryset, many=True)

        return Response(serialized_questions.data, status=status.HTTP_200_OK)


