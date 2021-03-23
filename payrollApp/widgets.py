from django.forms import widgets

class DateWithButtonWidget(widgets.DateInput):
    template_name = 'django/forms/widgets/select_date.html'