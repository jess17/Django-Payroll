from django.contrib import admin

from .models import Order, Employee, Process, Position, EmploymentType, CompletedProcess
# Register your models here.
admin.site.register(Order)
# admin.site.register(Employee)
# admin.site.register(Process)
admin.site.register(Position)
admin.site.register(EmploymentType)
# admin.site.register(CompletedProcess)

from admin_auto_filters.filters import AutocompleteFilter
class EmployeeFilter(AutocompleteFilter):
  title = 'Employee Name' # display title
  field_name = 'employeeID' # name of the foreign key field
    
class EmployeeAdmin(admin.ModelAdmin):
  search_fields = ['firstName'] # this is required for django's autocomplete functionality

class ProcessFilter(AutocompleteFilter):
  title = 'Process Name'
  field_name = "processID"

class ProcessAdmin(admin.ModelAdmin):
  search_fields = ['name'] # this is required for django's autocomplete functionality

class CompletedProcessAdmin(admin.ModelAdmin):
  list_filter = (EmployeeFilter, ProcessFilter)


# Register your models here.
admin.site.register(CompletedProcess, CompletedProcessAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Process, ProcessAdmin)
