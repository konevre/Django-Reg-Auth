import django.forms
import django_filters
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author, Category

class PostFilter(FilterSet):
    date = django_filters.DateFilter(
        field_name="date_posted",
        lookup_expr="gte",
        label="Date from",
        widget = django.forms.DateInput(
            attrs = {
                'type': 'date'
            }
        )
    )

    title = CharFilter(
        lookup_expr = 'icontains',
        label = 'Post Title'
    )

    author = ModelChoiceFilter(
        queryset = Author.objects.all(),
        label = 'Author'
    )

    category = ModelChoiceFilter(
        field_name = "post_category", 
        queryset = Category.objects.all(),
        label = 'Category'
    )
