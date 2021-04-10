from django.contrib import admin

from .models import Order, Employee, Process, Position, EmploymentType, CompletedProcess, DailySalary, Attendance, Allowance, Deduction
# Register your models here.
# admin.site.register(Order)
# admin.site.register(Employee)
# admin.site.register(Process)
# admin.site.register(Position)
# admin.site.register(EmploymentType)
# admin.site.register(CompletedProcess)

from admin_auto_filters.filters import AutocompleteFilter
class EmployeeFilter(AutocompleteFilter):
  title = 'Employee Name' # display title
  field_name = 'employeeID' # name of the foreign key field

class OrderFilter(AutocompleteFilter):
  title = 'Order Code' # display title
  field_name = 'orderID' # name of the foreign key field

class OrderAdmin(admin.ModelAdmin):
  search_fields = ['code', 'name']
  list_display = ('id', 'code', 'name', 'quantity')

class EmployeeAdmin(admin.ModelAdmin):
  search_fields = ['firstName', 'lastName'] # this is required for django's autocomplete functionality
  list_display = ('id', 'firstName', 'lastName', 'positionID', 'employmentTypeID', 'hireDate')

class ProcessFilter(AutocompleteFilter):
  title = 'Process Name'
  field_name = 'processID'

class ProcessAdmin(admin.ModelAdmin):
  list_filter = (OrderFilter, )
  search_fields = ['name', 'orderID__code', 'orderID__name'] 
  list_display = ('id', 'orderID', 'name', 'quantity')

class CompletedProcessAdmin(admin.ModelAdmin):
  list_filter = (EmployeeFilter, ProcessFilter)
  search_fields = ['processID__name', 'employeeID__firstName']
  list_display = ('processID', 'employeeID', 'quantity')

class PositionAdmin(admin.ModelAdmin):
  search_fields = ['name']

class EmploymentTypeAdmin(admin.ModelAdmin):
  search_fields = ['name']

class DailySalaryAdmin(admin.ModelAdmin):
  search_fields = ['employeeID__firstName', 'employeeID__lastName']
  list_display = ('employeeID', 'dailySalary', 'lastModified')

class AttendanceAdmin(admin.ModelAdmin):
  search_fields = ['employeeID__firstName', 'employeeID__lastName']
  list_filter = ('date', EmployeeFilter)
  list_display = ('employeeID', 'date', 'percentage')

class AllowanceAdmin(admin.ModelAdmin):
  search_fields = ['employeeID__firstName', 'employeeID__lastName']
  list_filter = ('date', EmployeeFilter)
  list_display = ('employeeID', 'amount', 'date')

class DeductionAdmin(admin.ModelAdmin):
  search_fields = ['employeeID__firstName', 'employeeID__lastName']
  list_filter = ('date', EmployeeFilter)
  list_display = ('employeeID', 'amount', 'date')

# Register your models here.
admin.site.register(CompletedProcess, CompletedProcessAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Process, ProcessAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(EmploymentType, PositionAdmin)
admin.site.register(DailySalary, DailySalaryAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Allowance, AllowanceAdmin)
admin.site.register(Deduction, DeductionAdmin)
