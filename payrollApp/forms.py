from django import forms

from .models import Order, Process, Employee, Position, EmploymentType
from django import forms

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = [
      'id',
      'code',
      'name',
      'quantity',
      'description',
      # 'dateCreated',
      # 'lastModified',
    ]

class ProcessForm(forms.ModelForm):
  class Meta:
    model = Process
    fields = [
      'id',
      'orderId',
      'name',
      'price',
      'quantity',
      'description',
    ]

  # firstName      = models.CharField(max_length=30)
  # lastName       = models.CharField(max_length=30, blank=True, null=True)
  # phoneNumber    = models.CharField(max_length=15, blank=True, null=True)
  # email          = models.CharField(max_length=100, blank=True, null=True)
  # address        = models.CharField(max_length=200, blank=True, null=True)
  # positionID     = models.ForeignKey('Position', default=None, null=True, on_delete=models.SET_DEFAULT)
  # employmentTypeID = models.ForeignKey('EmploymentType', default=None, null=True, on_delete=models.SET_DEFAULT)
  # hireDate       = models.DateTimeField(auto_now_add=True)
  # terminationDate= models.DateTimeField(blank=True, null=True)
  # notes          = models.TextField(blank=True, null=True)
class EmployeeForm(forms.ModelForm):
  firstName = forms.CharField(max_length=30,
   label='First Name',
    widget=forms.TextInput(attrs={"placeholder": "First Name"}))
  lastName          = forms.CharField(max_length=30, label='Last Name', required=False)
  phoneNumber       = forms.CharField(max_length=15, label='Phone Number', required=False)
  email             = forms.EmailField(label='Email', required=False)
  address           = forms.CharField(max_length=200, label='Address', required=False)
  # forms.ModelChoiceField(queryset=Speed.objects.all())
  positionID        = forms.ModelChoiceField(queryset=Position.objects.all(),label='Position ID', required=False)
  employmentTypeID  = forms.ModelChoiceField(queryset=EmploymentType.objects.all(), label='Employment Type ID', required=False)
  terminationDate   = forms.DateTimeField(label='Termination Date', required=False,
        widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),)

  class Meta:
    model = Employee
    fields = [
      'id',
      'firstName',
      'lastName',
      'phoneNumber',
      'email',
      'address',
      'positionID',
      'employmentTypeID',
      'terminationDate',
      'notes',
    ]

class PositionForm(forms.ModelForm):
  class Meta:
    model = Position
    fields = [
      'id',
      'name',
    ]

class EmploymentTypeForm(forms.ModelForm):
  class Meta:
    model = EmploymentType
    fields = [
      'id',
      'name',
      'description'
    ]