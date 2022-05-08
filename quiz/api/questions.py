import logging
from typing import List

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.api.docs import GetQuestionsParameters
from quiz.models import Question, Answer
from quiz.serializers import (
    GetQuestionsRequestSerializer,
    QuestionSerializer,
    UserAnswerSerializer,
    AnswerCheckResponseSerializer
)
from quiz.utils.db.question import QuestionQueryFacade


logger = logging.getLogger(__name__)


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

        # filter questions that have at least one right answer
        queryset = queryset.annotate(
            have_right_answers=QuestionQueryFacade.annotate_has_right_questions()
        ).filter(have_right_answers=True).order_by('?')

        queryset = queryset[:request_data.get('questions_count')]
        serialized_questions = QuestionSerializer(queryset, many=True)

        return Response(serialized_questions.data, status=status.HTTP_200_OK)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_id='Проверка ответов на правильность',
        responses={
            status.HTTP_200_OK: AnswerCheckResponseSerializer()
        },
        request_body=UserAnswerSerializer(many=True),
    )
)
class CheckAnswersView(GenericAPIView):
    """Check answers and return detail."""

    queryset = Answer.objects.all()

    def post(self, request: Request, *args, **kwargs):
        request_serializer = UserAnswerSerializer(data=request.data, many=True)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_answers_request = request_serializer.validated_data
        total = 0
        right = 0
        check_result: List[dict] = []

        for user_answer_request in user_answers_request:
            question_id = user_answer_request.get('question_id')
            user_answer_id = user_answer_request.get('answer_id')
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                logger.warning(f'Question with ID {question_id} does not exist.')
                continue
            total += 1
            right_answer = question.answers.filter(right=True).first()
            if user_answer_id == right_answer.id:
                right += 1
                check_result.append(
                    {
                        'is_right': True,
                        'right_answer_id': right_answer.id,
                        'right_answer_description': right_answer.description
                    }
                )
            else:
                try:
                    user_answer = question.answers.get(id=user_answer_id)
                except Answer.DoesNotExist:
                    logger.warning(f'Answer with ID {question_id} does not exist.')
                    user_answer = None
                if user_answer:
                    check_result.append(
                        {
                            'is_right': False,
                            'right_answer_id': right_answer.id,
                            'right_answer_description': right_answer.description,
                            'user_answer_id': user_answer.id,
                            'user_answer_description': user_answer.description,
                        }
                    )
                else:
                    check_result.append(
                        {
                            'is_right': False,
                            'right_answer_id': right_answer.id,
                            'right_answer_description': right_answer.description,
                        }
                    )
        result = AnswerCheckResponseSerializer(data={
            'right': right,
            'total': total,
            'check_result': check_result
        })
        result.is_valid()

        return Response(result.validated_data)



