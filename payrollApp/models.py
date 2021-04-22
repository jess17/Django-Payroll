from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# from django.db.models import Q
# from django.db.models import constraints
from django.db.models import Sum

# Create your models here.
class Order(models.Model):
  code         = models.CharField(max_length=50, unique=True)
  name         = models.CharField(max_length=200)
  quantity     = models.PositiveIntegerField()
  description  = models.TextField(blank=True, null=True) 
  dateCreated  = models.DateTimeField(auto_now_add=True)
  lastModified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.id)+" | "+self.code

class Process(models.Model):
  orderID     = models.ForeignKey('Order', default=None, null=True, on_delete=models.CASCADE)
  name        = models.CharField(max_length=200)
  price       = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0, message="Price can't be less than 0")])
  quantity    = models.PositiveIntegerField()
  description = models.TextField(blank=True, null=True)

  # class Meta:
  #       constraints = [
  #           constraints.CheckConstraint(
  #               check=Q(price__gte=0),
  #               name='price_positive'
  #           )
  #       ]

  def __str__(self):
    return str(self.id)+" | "+self.name

class Employee(models.Model):
  firstName      = models.CharField(max_length=30)
  lastName       = models.CharField(max_length=30, blank=True, null=True)
  phoneNumber    = models.CharField(max_length=15, blank=True, null=True)
  email          = models.CharField(max_length=100, blank=True, null=True)
  address        = models.CharField(max_length=200, blank=True, null=True)
  positionID     = models.ForeignKey('Position', default=None, null=True, on_delete=models.SET_DEFAULT, blank=True)
  employmentTypeID = models.ForeignKey('EmploymentType', default=None, null=True, on_delete=models.SET_DEFAULT, blank=True)
  hireDate       = models.DateTimeField(auto_now_add=True)
  terminationDate= models.DateTimeField(blank=True, null=True)
  notes          = models.TextField(blank=True, null=True)

  def __str__(self):
    if self.lastName:
      return str(self.id)+" | "+self.firstName.capitalize()+" "+self.lastName.capitalize()
    else:
      return str(self.id)+" | "+self.firstName.capitalize()

class Position(models.Model):
  name = models.CharField(max_length=60, unique=True)

  def __str__(self):
    return self.name

class EmploymentType(models.Model):
  name        = models.CharField(max_length=60, unique=True)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name

class CompletedProcess(models.Model):
  processID     = models.ForeignKey('Process', default=None, null=True, on_delete=models.CASCADE)
  employeeID    = models.ForeignKey('Employee', default=None, null=True, on_delete=models.CASCADE)
  
  # from .forms import CompletedProcessForm
  # currentProcessID = CompletedProcessForm(request.POST).cleaned_data['processID']
  # processQty  = getattr(Process.objects.get(id=currentProcessId), 'quantity')
  # completedProcessQty = CompletedProcess.objects.filter(processId=currentProcessId).aggregate(maxVal=Sum('quantity'))
  # maxVal = processQty-completedProcessQty
  # quantity      = models.PositiveIntegerField(validators=[MaxValueValidator(maxVal, message="Quantity can't be greater than"+str(maxVal))])
  quantity      = models.PositiveIntegerField(validators=[MinValueValidator(1, message="Quantity can't be less than 1")])
  dateRecorded  = models.DateTimeField(auto_now_add=True)

  def clean(self):
    # print("Process ID after split: ", int(str(self.processID).split("|")[0]))
    currentProcessID    = int(str(self.processID).split("|")[0])
    processQty          = getattr(Process.objects.get(id=currentProcessID), 'quantity')
    completedProcessQty = CompletedProcess.objects.filter(processID=currentProcessID).exclude(id=self.id).aggregate(completedProcessQty=Sum('quantity'))
    
    if completedProcessQty['completedProcessQty'] != None:
      maxVal = processQty - completedProcessQty['completedProcessQty']
    #No completed process of this process
    else:
      maxVal = processQty
    
    if self.quantity > maxVal:
      # print("Sth is wrong")
      errMsg = "Quantity can't be greater than " + str(maxVal)
      raise ValidationError(errMsg)
    # print("Nothing is wrong")
    # return cleaned_data

  def __str__(self):
    return str(self.processID) + " | " + str(self.employeeID)

class DailySalary(models.Model):
  employeeID    = models.OneToOneField('Employee', on_delete=models.CASCADE, unique=True)
  dailySalary   = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0, message="Daily salary can't be smaller than 0")])
  notes         = models.TextField(blank=True, null=True)
  lastModified  = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
  # ONTIME = 1
  # LATE = 2
  # ABSENT = 3
  # ONLEAVE = 4

  # STATUS_CHOICES = {
  #   (ONTIME, "On time"),
  #   (LATE, "Late"),
  #   (ABSENT, "Absent"),
  # }

  employeeID    = models.ForeignKey('Employee', default=None, null=True, on_delete=models.CASCADE)
  date          = models.DateField()
  percentage    = models.IntegerField(default=100, validators=[MinValueValidator(0, message="Can't be less than 0"), MaxValueValidator(100, message="Can't be greater than 100")])
  # status        = models.IntegerField(choices= STATUS_CHOICES)

  class Meta:
    unique_together = [['employeeID', 'date']]

class Allowance(models.Model):
  employeeID  = models.ForeignKey('Employee', default=None, null=True, on_delete=models.CASCADE)
  amount      = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0.01, message="Amount must be greater than 0")])
  description = models.CharField(max_length=200, null=True, blank=True)
  date        = models.DateField()

class Deduction(models.Model):
  employeeID  = models.ForeignKey('Employee', default=None, null=True, on_delete=models.CASCADE)
  amount      = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0.01, message="Amount must be greater than 0")])
  description = models.CharField(max_length=200, null=True, blank=True)
  date        = models.DateField()
  

  

