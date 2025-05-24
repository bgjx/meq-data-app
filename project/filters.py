import django_filters
from django import forms
from django_filters import DateFilter
from django.apps import apps
from django.db.models import Min, Max

def dynamic_filter(model_name):
    picked_model = apps.get_model('project', model_name)

    # get the data time scope
    min_date = picked_model.objects.all().aggregate(min_date=Min('dt_origin'))['min_date']
    max_date = picked_model.objects.all().aggregate(max_date=Max('dt_origin'))['max_date']

    class MyFilter(django_filters.FilterSet):
        start_date = DateFilter(field_name="dt_origin", 
                                lookup_expr="gte", 
                                label="Start Date",
                                widget = forms.DateInput(
                                    attrs={
                                        'type': 'date',
                                        'min': min_date.strftime('%Y-%m-%d') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d') if max_date else ''
                                    }
                                ))
        end_date = DateFilter(field_name="dt_origin",
                              lookup_expr="lte", 
                              label="End Date",
                              widget = forms.DateInput(
                                  attrs={
                                        'type': 'date',
                                        'min': min_date.strftime('%Y-%m-%d') if min_date else '',
                                        'max': max_date.strftime('%Y-%m-%d') if max_date else ''
                                  }
                              ))
        class Meta:
            model = picked_model
            fields = []
    return MyFilter







