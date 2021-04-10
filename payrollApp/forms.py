from django import forms


from .models import Order, Process, Employee, Position, EmploymentType, CompletedProcess, DailySalary, Attendance
from .models import Allowance, Deduction

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
  username = forms.CharField(max_length=100, required=True)
  password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = {"username", "password"}

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
  # Get ID from arg pass in process_edit_view
  def __init__(self, *args, **kwargs):
    self._id = kwargs.pop('id', None)
    super().__init__(*args, **kwargs)

  orderID     = forms.ModelChoiceField(queryset=Order.objects.all().order_by('-id'),label='Order Code')

  
  def clean_quantity(self):
    processIDVal = self._id
    completedProcessesQty = CompletedProcess.objects.filter(processID=processIDVal).values('quantity')
    
    completedQty = 0
    for completedProcessQty in completedProcessesQty:
      completedQty = completedQty + completedProcessQty['quantity']
    print("Completed quantity: ", completedQty)

    if int(self['quantity'].value())<completedQty:
        errorMsg = "Quantity is smaller than completed quantity ("+ str(completedQty) + ")"
        # raise ValidationError(errorMsg)    
        raise ValidationError(
          ('Quantity can\'t be smaller than the completed quantity %(completedQty)s'),
          code='Quantity',
          params={'completedQty': completedQty},
        )

    return self['quantity'].value()

  class Meta:
    model = Process
    fields = [
      'id',
      'orderID',
      'name',
      'price',
      'quantity',
      'description',
    ]

class EmployeeForm(forms.ModelForm):
  firstName = forms.CharField(max_length=30,
   label='First Name',
    widget=forms.TextInput(attrs={"placeholder": "First Name"}))
  lastName          = forms.CharField(max_length=30, label='Last Name', required=False)
  phoneNumber       = forms.CharField(max_length=15, label='Phone Number', required=False)
  email             = forms.EmailField(label='Email', required=False)
  address           = forms.CharField(max_length=200, label='Address', required=False)
  # forms.ModelChoiceField(queryset=Speed.objects.all())
  positionID        = forms.ModelChoiceField(queryset=Position.objects.all(),label='Position', required=False)
  employmentTypeID  = forms.ModelChoiceField(queryset=EmploymentType.objects.all(), label='Employment Type', required=False)
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

class CompletedProcessForm(forms.ModelForm):
  processID = forms.ModelChoiceField(
    queryset=Process.objects.all().order_by('-id'), 
    label='Process ID', required=True, 
    # widget=forms.AutocompleteSelectWidget()
    )
  employeeID = forms.ModelChoiceField(queryset=Employee.objects.all(),label='Employee ID', required=True)
  

  class Meta:
    model = CompletedProcess
    fields = [
      'processID',
      'employeeID',
      'quantity'
    ]

class DailySalaryForm(forms.ModelForm):
  employeeID = forms.ModelChoiceField(
    queryset=Employee.objects.all(), 
    label='Employee ID', required=True
  )
  dailySalary = forms.DecimalField(label='Daily Salary')

  class Meta:
    model = DailySalary
    fields = [
      'employeeID',
      'dailySalary',
      'notes'
    ]

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class GetDateForm(forms.Form):
  startDate = forms.DateField(label='From', required=True, widget=DateInput())
  endDate   = forms.DateField(label='To', required=True, widget=DateInput())
  
  def clean(self):
    cleaned_data = super().clean()
    startDate = cleaned_data.get("startDate")
    endDate = cleaned_data.get("endDate")
    if endDate < startDate:
        raise forms.ValidationError("End date should be greater than start date")

class AttendanceForm(forms.ModelForm):
  employeeID  = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('-id'), label='Employee', required=True)
  date   = forms.DateField(label='Date', required=True, widget=DateInput())
  
  class Meta:
    model = Attendance
    fields = [
      'employeeID',
      'date',
      'percentage'
    ]

class ChooseEmployeeForm(forms.Form):
  employeeID  = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('-id'), label='Employee', required=True)

class AllowanceForm(forms.ModelForm):
  employeeID  = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('-id'), label='Employee', required=True)
  date   = forms.DateField(label='Date', required=True, widget=DateInput())
  
  class Meta:
    model = Allowance
    fields = [
      'employeeID',
      'amount',
      'description',
      'date'
    ]

class DeductionForm(forms.ModelForm):
  employeeID  = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('-id'), label='Employee', required=True)
  date   = forms.DateField(label='Date', required=True, widget=DateInput())
  
  class Meta:
    model = Deduction
    fields = [
      'employeeID',
      'amount',
      'description',
      'date'
    ]



