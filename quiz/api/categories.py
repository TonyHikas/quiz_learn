from dal import autocomplete

from quiz.models import Category


class CategoriesAutocomplete(autocomplete.Select2QuerySetView):
    """Endpoint for category autocomplete select."""

    def get_queryset(self):
        queryset = Category.objects.all()
        if self.q:
            queryset = queryset.filter(name__icontains=self.q)
        return queryset

    def get_result_label(self, result):
        return result.name
