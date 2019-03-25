from django.contrib.auth.models import User
import django_filters
from .models import Post, Profile

class PostFilter(django_filters.FilterSet):
    # datetime = django_filters.NumberFilter(name='datetime', lookup_expr='year')
    # author = django_filters.ModelChoiceFilter(queryset=Profile.objects.all())
    class Meta:
        model = Post
        fields = {'datetime': ['gt'],
                  'author':['exact']}

    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    # year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    # groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),widget=forms.CheckboxSelectMultiple)
    #
    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'year_joined', 'groups']