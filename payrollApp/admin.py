from django.contrib import admin

from .models import Order, Employee, Process, Position, EmploymentType
# Register your models here.
admin.site.register(Order)
admin.site.register(Employee)
admin.site.register(Process)
admin.site.register(Position)
admin.site.register(EmploymentType)
