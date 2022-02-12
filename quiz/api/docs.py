from drf_yasg import openapi

GetQuestionsParameters = [
    openapi.Parameter(
        type=openapi.TYPE_INTEGER,
        in_=openapi.IN_QUERY,
        name='category_id',
        description='ID of category',
        default=None
    ),
    openapi.Parameter(
        type=openapi.TYPE_INTEGER,
        in_=openapi.IN_QUERY,
        name='questions_count',
        description='Количество вопросов',
        default=5
    )
]
