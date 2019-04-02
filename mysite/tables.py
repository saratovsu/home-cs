import django_tables2 as tables
from .models import Meter

class MeterTable(tables.Table):
    class Meta:
        model = Meter
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id',)