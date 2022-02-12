from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Coalesce

from quiz.models import Answer


class QuestionQueryFacade:
    """Facade for get query annotations for Question model."""

    @staticmethod
    def annotate_has_right_questions() -> Coalesce:
        """Return False if question have no right answers."""
        return Coalesce(
            Subquery(
                Answer.objects.filter(
                    question_id=OuterRef('id'),
                    right=True
                ).values('right')[:1]
            ),
            Value(False)
        )
