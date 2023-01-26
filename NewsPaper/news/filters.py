from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import *


class SeArch(FilterSet):
    title = CharFilter(field_name='title', label='Название содержит', lookup_expr='icontains')
    category = ModelChoiceFilter(field_name='postCategory', queryset=Category.objects.all(),
                                 label='Категория', empty_label='Выберите категорию',)
    date_choices = DateTimeFilter(field_name='dateCreation', lookup_expr='gt', label='Позже даты',
                                  widget=DateTimeInput(attrs={'type': 'datetime-local'},), )
