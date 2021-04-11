import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *
from django import forms

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class OrderFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="dateCreated", lookup_expr='gte', widget=DateInput(), label="Date Created is greater than or equal to")
  end_date = DateFilter(field_name="dateCreated", lookup_expr='lte', widget=DateInput(), label='Date Created is less than or equal to')
  code = CharFilter(field_name="code", lookup_expr='icontains')
  description = CharFilter(field_name="description", lookup_expr='icontains')

  class Meta:
    model = Order 
    fields =  '__all__'
    exclude = ['lastModified', 'dateCreated', 'quantity']

class AllowanceFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="date", lookup_expr='gte', widget=DateInput(), label="Date is greater than or equal to")
  end_date = DateFilter(field_name="date", lookup_expr='lte', widget=DateInput(), label='Date is less than or equal to')
  description = CharFilter(field_name="description", lookup_expr='icontains')

  class Meta:
    model = Allowance 
    fields =  '__all__'
    exclude = ['amount', 'date']

class DeductionFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="date", lookup_expr='gte', widget=DateInput(), label="Date is greater than or equal to")
  end_date = DateFilter(field_name="date", lookup_expr='lte', widget=DateInput(), label='Date is less than or equal to')
  description = CharFilter(field_name="description", lookup_expr='icontains')

  class Meta:
    model = Deduction 
    fields =  '__all__'
    exclude = ['amount', 'date']

class EmployeeFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="hireDate", lookup_expr='gte', widget=DateInput(), label="Date Hired is greater than or equal to")
  end_date = DateFilter(field_name="hireDate", lookup_expr='lte', widget=DateInput(), label='Date Hired is less than or equal to')
  firstName = CharFilter(field_name="firstName", lookup_expr='icontains', label='First Name')
  lastName = CharFilter(field_name="lastName", lookup_expr='icontains', label='Last Name')
  notes    = CharFilter(field_name="notes", lookup_expr='icontains')

  class Meta:
    model = Employee 
    fields =  '__all__'
    exclude = ['hireDate', 'terminationDate']

class CompletedProcessFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="dateRecorded", lookup_expr='gte', widget=DateInput(), label="Date Recorded is greater than or equal to: ")
  end_date = DateFilter(field_name="dateRecorded", lookup_expr='lte', widget=DateInput(), label='Date Recorded is less than or equal to: ')

  class Meta:
    model = CompletedProcess 
    fields =  '__all__'
    exclude = ['quantity', 'dateRecorded']

class CompletedProcessOfProcessFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="dateRecorded", lookup_expr='gte', widget=DateInput(), label="Date Recorded is greater than or equal to: ")
  end_date = DateFilter(field_name="dateRecorded", lookup_expr='lte', widget=DateInput(), label='Date Recorded is less than or equal to: ')

  class Meta:
    model = CompletedProcess 
    fields =  '__all__'
    exclude = ['processID', 'quantity', 'dateRecorded']

class CompletedProcessOfEmployeeFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="dateRecorded", lookup_expr='gte', widget=DateInput(), label="Date Recorded is greater than or equal to: ")
  end_date = DateFilter(field_name="dateRecorded", lookup_expr='lte', widget=DateInput(), label='Date Recorded is less than or equal to: ')
  
  class Meta:
    model = CompletedProcess 
    fields =  '__all__'
    exclude = ['employeeID', 'quantity', 'dateRecorded']

class ProcessFilter(django_filters.FilterSet):
  name = CharFilter(field_name="name", lookup_expr='icontains')
  description = CharFilter(field_name="description", lookup_expr='icontains')
  start_price = NumberFilter(field_name="price", lookup_expr='gte')
  end_price = NumberFilter(field_name="price", lookup_expr='lte')

  class Meta:
    model = Process 
    fields =  '__all__'
    exclude = ['quantity', 'price']

class ProcessOfOrderFilter(django_filters.FilterSet):
  name = CharFilter(field_name="name", lookup_expr='icontains')
  description = CharFilter(field_name="description", lookup_expr='icontains')
  start_price = NumberFilter(field_name="price", lookup_expr='gte')
  end_price = NumberFilter(field_name="price", lookup_expr='lte')

  class Meta:
    model = Process 
    fields =  '__all__'
    exclude = ['quantity', 'price', 'orderID']

class AttendanceFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="date", lookup_expr='gte', widget=DateInput(), label="Date is greater than or equal to")
  end_date = DateFilter(field_name="date", lookup_expr='lte', widget=DateInput(), label='Date is less than or equal to')
  start_percentage = NumberFilter(field_name="percentage", lookup_expr='gte')
  end_percentage = NumberFilter(field_name="percentage", lookup_expr='lte')

  class Meta:
    model = Attendance 
    fields =  '__all__'
    exclude = ['date', 'percentage']

class AttendanceOfEmployeeFilter(django_filters.FilterSet):
  start_date = DateFilter(field_name="date", lookup_expr='gte', widget=DateInput(), label="Date is greater than or equal to")
  end_date = DateFilter(field_name="date", lookup_expr='lte', widget=DateInput(), label='Date is less than or equal to')
  start_percentage = NumberFilter(field_name="percentage", lookup_expr='gte')
  end_percentage = NumberFilter(field_name="percentage", lookup_expr='lte')

  class Meta:
    model = Attendance 
    fields =  '__all__'
    exclude = ['date', 'percentage', 'employeeID']

