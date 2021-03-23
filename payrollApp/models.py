from django.db import models

from django.core.validators import MinValueValidator
from django.db.models import Q
from django.db.models import constraints

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
  orderId     = models.ForeignKey('Order', default=None, null=True, on_delete=models.SET_DEFAULT)
  name        = models.CharField(max_length=200)
  price       = models.DecimalField(decimal_places=2, max_digits=100, validators=[MinValueValidator(0, message="Price can't be less than 0")])
  quantity    = models.PositiveIntegerField()
  description = models.TextField(blank=True, null=True)

  class Meta:
        constraints = [
            constraints.CheckConstraint(
                check=Q(price__gte=0),
                name='price_positive'
            )
        ]

  def __str__(self):
    return str(self.id)+". "+self.name

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
    return str(self.id)+" | "+self.firstName

class Position(models.Model):
  name = models.CharField(max_length=60)

  def __str__(self):
    return self.name

class EmploymentType(models.Model):
  name        = models.CharField(max_length=60)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name


