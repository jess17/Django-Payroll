from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
from django.contrib import messages
# from django.core.exceptions import ValidationError


# from django.urls import reverse
from datetime import date, datetime, timedelta
from django.forms import inlineformset_factory
from django.forms import formset_factory

from .models import Order, Process, Employee, EmploymentType, Position, CompletedProcess, DailySalary, Attendance
from .forms import OrderForm, ProcessForm, EmployeeForm, PositionForm, EmploymentTypeForm, CompletedProcessForm, DailySalaryForm, GetDateForm, AttendanceForm, ChooseEmployeeForm
# Create your views here.
def home_view(request):
    return render(request, "real_base.html", {})

def edit(request, object_id, Form, Object, redirectVal, returnLoc):
  form = Form(instance=Object.objects.get(id=object_id))

  if request.method == "POST":
      form = Form(request.POST, request.FILES, instance=Object.objects.get(id=object_id))

      if form.is_valid():
          form.save()
          return redirectVal
  return render(request, returnLoc, {
      "form": form
  })

def delete(request, Object):
  if request.method == "POST":
    idList = request.POST.getlist("selected")
  for i in idList:
    Object.objects.get(id=i).delete()
  if idList:
    messages.success(request, "Selected rows has been deleted successfully")
  else:
    messages.info(request, "Nothing is selected")


#ORDER RELATED VIEWS
def order_view(request):
  orders = Order.objects.all().order_by('-lastModified')
  flag   = True
  if not orders:
    flag=False
    
  context = {
    'orders':orders,
    'flags': flag
  }
  return render(request, "order/order.html", context)

def order_create_view(request):
  form = OrderForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect(order_view)

  context = {
    'form':form
  }
  return render(request, "order/order_create.html", context)

def order_edit_view(request, order_id):
  return edit(request, order_id, OrderForm, Order, redirect(request.GET.get("next")), 'order/order_edit.html')
    # form = OrderForm(instance=Order.objects.get(id=order_id))

    # if request.method == "POST":
    #     form = OrderForm(request.POST, request.FILES, instance=Order.objects.get(id=order_id))

    #     if form.is_valid():
    #       form.save()
          
    #       return redirect(request.GET.get("next"))

    # return render(request, 'order/order_edit.html', {
    #     "form": form
    # })

def order_delete_view(request):
  delete(request, Order)
  return redirect(request.GET.get("next"))








#PROCESS RELATED VIEWS
def process_view(request):
  processes = Process.objects.all().order_by('-id')
  flag   = True
  if not processes:
    flag=False

  orders = Order.objects.exists()
  orderFlag=True
  if not orders:
    #Orders is empty
    orderFlag=False

  context = {
    'processes':processes,
    'orderFlag':orderFlag,
    'flags':flag,
  }
  return render(request, "process/process.html", context)

def process_of_order_view(request, order_id):
  order = Order.objects.get(id=order_id)
  processes = Process.objects.filter(orderID=order_id)

  if processes:
    #There's at least one process
    flag=True
  else:
    flag=False
  
  context = {
    'processes':processes,
    'flags':flag,
    'order':order,
  }
  return render(request, "process/process_of_order.html", context)

# def process_of_order_view(request, order_code):
#   processes = Process.objects.filter(orderID=order_code)
#   # processes = Process.objects.get(id=order_id)
#   if processes:
#     #There's at least one process
#     flag=True
#   else:
#     flag=False

#   context = {
#     'processes':processes,
#     'flags':flag,
#     'orderID':order_id,
#   }
#   return render(request, "process/process_of_order.html", context)

def process_create_view(request):
  form = ProcessForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "process/process_create.html", context)

def process_order_create_view(request, order_id):
  form = ProcessForm(request.POST or None)
  form.fields['orderID'].initial = order_id
  form.fields['orderID'].disabled = True
  order = Order.objects.get(id=order_id)
  form.fields['quantity'].initial = order.quantity


  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "process/process_create.html", context)

def process_edit_view(request, process_id):
  return edit(request, process_id, ProcessForm, Process, redirect(request.GET.get("next")), 'process/process_edit.html')
  # form = ProcessForm(instance=Process.objects.get(id=process_id))
  
  # # print("Completed quantity: ", completedQty)

  # # print(form['quantity'].value())
  

  # if request.method == "POST":
  #   # print("Process ID (View): ", process_id)
  #   form = ProcessForm(request.POST, request.FILES, instance=Process.objects.get(id=process_id), id=process_id)


  #   if form.is_valid():
  #       form.save()
  #       # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  #       return redirect(request.GET.get("next"))

  # return render(request, 'process/process_edit.html', {
  #     "form": form,
  # })

def process_delete_view(request):
  delete(request, Process)
  return redirect(request.GET.get("next"))







#EMPLOYEE RELATED VIEWS
def employee_view(request):
  employees = Employee.objects.all()
  flag   = True
  if not employees:
    flag=False

  context = {
    'employees':employees,
    'flags':flag
  }
  return render(request, 'employee/employee.html', context)

def employee_create_view(request):
  form = EmployeeForm(request.POST or None)
  # positions = Position.objects.all()
  # employmentTypes = EmploymentType.objects.all()

  if form.is_valid():
    form.save()
    return redirect(employee_view)

  context = {
    'form':form,
    # 'positions': positions,
    # 'employmentTypes': employmentTypes
  }
  return render(request, "employee/employee_create.html", context)

def employee_edit_view(request, employee_id):
  return edit(request, employee_id, EmployeeForm, Employee, redirect(request.GET.get("next")), 'employee/employee_edit.html')
  # form = EmployeeForm(instance=Employee.objects.get(id=employee_id))

  # if request.method == "POST":
  #     form = EmployeeForm(request.POST, request.FILES, instance=Employee.objects.get(id=employee_id))

  #     if form.is_valid():
  #         form.save()
  #         return redirect(request.GET.get("next"))

  # return render(request, 'employee/employee_edit.html', {
  #     "form": form
  # })

def employee_delete_view(request):
  delete(request, Employee)
  return redirect(employee_view)











#POSITION RELATED VIEWS
def position_view(request):
  positions = Position.objects.all()
  flag   = True
  if not positions:
    flag=False

  context = {
    'positions':positions,
    'flags':flag
  }
  return render(request, 'employee/position/position.html', context)

def position_create_view(request):
  form = PositionForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "employee/position/position_create.html", context)

def position_edit_view(request, position_id):
  return edit(request, position_id, PositionForm, Position, redirect(request.GET.get("next")), 'employee/position/position_edit.html')

    # form = PositionForm(instance=Position.objects.get(id=position_id))

    # if request.method == "POST":
    #     form = PositionForm(request.POST, request.FILES, instance=Position.objects.get(id=position_id))

    #     if form.is_valid():
    #         form.save()
    #         return redirect(request.GET.get("next"))

    # return render(request, 'employee/position/position_edit.html', {
    #     "form": form
    # })

def position_delete_view(request):
  delete(request, Position)
  return redirect(position_view)











#EMPLOYMENT TYPE RELATED VIEWS
def employmentType_view(request):
  employmentTypes = EmploymentType.objects.all()
  flag   = True
  if not employmentTypes:
    flag=False

  context = {
    'employmentTypes':employmentTypes,
    'flags':flag
  }
  return render(request, 'employee/employmentType/employmentType.html', context)

def employmentType_create_view(request):
  form = EmploymentTypeForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "employee/employmentType/employmentType_create.html", context)

def employmentType_edit_view(request, employmentType_id):
  return edit(request, employmentType_id, EmploymentTypeForm, EmploymentType, redirect(request.GET.get("next")), 'employee/employmentType/employmentType_edit.html')

  # form = EmploymentTypeForm(instance=EmploymentType.objects.get(id=employmentType_id))

  # if request.method == "POST":
  #     form = EmploymentTypeForm(request.POST, request.FILES, instance=EmploymentType.objects.get(id=employmentType_id))

  #     if form.is_valid():
  #         form.save()
  #         return redirect(request.GET.get("next"))

  # return render(request, 'employee/employmentType/employmentType_edit.html', {
  #     "form": form
  # })

def employmentType_delete_view(request):
  delete(request, EmploymentType)
  return redirect(employmentType_view)












#COMPLETED PROCESS RELATED VIEWS
def completedProcess_view(request):
  completedProcesses = CompletedProcess.objects.all().order_by('-id')
  flag   = True
  if not completedProcesses:
    flag=False

  processes = Process.objects.exists()
  processFlag=True
  if not processes:
    #Orders is empty
    processFlag=False

  context = {
    'completedProcesses':completedProcesses,
    'processFlag':processFlag,
    'flags':flag,
  }
  return render(request, "completedProcess/completedProcess.html", context)

def completedProcess_of_process_view(request, process_id):
  process = Process.objects.get(id=process_id)
  completedProcesses = CompletedProcess.objects.filter(processID=process_id).order_by('-dateRecorded')

  #Count total completed quantity of current process
  completedProcessesQty = completedProcesses.values('quantity')
  completedQty=0
  for completedProcessQty in completedProcessesQty:
    completedQty = completedQty + completedProcessQty['quantity']

  if completedProcesses:
    #There's at least one completedProcess
    flag=True
  else:
    flag=False
  
  context = {
    'completedProcesses':completedProcesses,
    'flags':flag,
    'process':process,
    'completedQty':completedQty
  }
  return render(request, "completedProcess/completedProcess_of_process.html", context)

def completedProcess_of_employee_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  completedProcesses = CompletedProcess.objects.filter(employeeID=employee_id).order_by('-dateRecorded')

  if completedProcesses:
    #There's at least one completedProcess
    flag=True
  else:
    flag=False
  
  context = {
    'completedProcesses':completedProcesses,
    'flags':flag,
    'employee':employee,
  }
  return render(request, "completedProcess/completedProcess_of_employee.html", context)

def completedProcess_create_view(request):
  form = CompletedProcessForm(request.POST or None)
  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "completedProcess/completedProcess_create.html", context)

def completedProcess_process_create_view(request, process_id):
  form = CompletedProcessForm(request.POST or None)
  form.fields['processID'].initial = process_id
  form.fields['processID'].disabled = True
  process = Process.objects.get(id=process_id)
  # form.fields['quantity'].initial = process.quantity


  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form,

  }
  return render(request, "completedProcess/completedProcess_create.html", context)

def completedProcess_employee_create_view(request, employee_id):
  form = CompletedProcessForm(request.POST or None)
  form.fields['employeeID'].initial = employee_id
  form.fields['employeeID'].disabled = True
  # employee = Employee.objects.get(id=employee_id)
  # form.fields['quantity'].initial = process.quantity


  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "completedProcess/completedProcess_create.html", context)

def completedProcess_edit_view(request, completedProcess_id):
  return edit(request, completedProcess_id, CompletedProcessForm, CompletedProcess, redirect(request.GET.get("next")), 'completedProcess/completedProcess_edit.html')

  # form = CompletedProcessForm(instance=CompletedProcess.objects.get(id=completedProcess_id))

  # if request.method == "POST":
  #     form = CompletedProcessForm(request.POST, request.FILES, instance=CompletedProcess.objects.get(id=completedProcess_id))
      
  #     # errMsg = "Quantity can't be greater than " + str(maxVal)
  #     # raise ValidationError(errMsg)
  #     if form.is_valid():
  #         form.save()
  #         # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  #         return redirect(request.GET.get("next"))

  # return render(request, 'completedProcess/completedProcess_edit.html', {
  #     "form": form
  # })

def completedProcess_delete_view(request):
  delete(request, CompletedProcess)
  return redirect(request.GET.get("next"))












#DAILY SALARY RELATED VIEWS
def dailySalary_view(request):
  dailySalaries = DailySalary.objects.all()
  flag   = True
  if not dailySalaries:
    flag=False

  context = {
    'dailySalaries':dailySalaries,
    'flags':flag
  }
  return render(request, 'salary/dailySalary.html', context)

def dailySalary_create_view(request):
  form = DailySalaryForm(request.POST or None)
  # employees = Employee.objects.all()

  if form.is_valid():
    form.save()
    return redirect(dailySalary_view)

  context = {
    'form':form,
    # 'employees': employees,
  }
  return render(request, "salary/dailySalary_create.html", context)

def dailySalary_edit_view(request, dailySalary_id):
  return edit(request, dailySalary_id, DailySalaryForm, DailySalary, redirect(dailySalary_view), 'salary/dailySalary_edit.html')
  # form = DailySalaryForm(instance=DailySalary.objects.get(id=dailySalary_id))

  # if request.method == "POST":
  #     form = DailySalaryForm(request.POST, request.FILES, instance=DailySalary.objects.get(id=dailySalary_id))

  #     if form.is_valid():
  #         form.save()
  #         return redirect(dailySalary_view)

  # return render(request, 'salary/dailySalary_edit.html', {
  #     "form": form
  # })

def dailySalary_delete_view(request):
  delete(request, DailySalary)
  return  redirect(dailySalary_view)















#SALARY RELATED VIEWS
class Salary:
  def __init__(self, employeeID, salary, pieceRate):
    self.employeeID = employeeID
    self.salary = salary
    self.pieceRate = pieceRate
    self.total = salary+pieceRate

def salary_view(request):
  start = request.session.get("startDate")
  end = request.session.get("endDate")
  # print(start)
  # print(end)

  # endPlus1 is needed cuz date__range is inclusive
  endPlus1 = datetime.strptime(end, "%Y-%m-%d")
  endPlus1 = endPlus1 + timedelta(days=1)
  completedProcesses = CompletedProcess.objects.filter(dateRecorded__range=[start, endPlus1])
  employees = Employee.objects.all()

  salaries = []
  i = 0
  for employee in employees:
    # print("Employee", employee)
    pieceRate = 0
    currCompletedProcesses = completedProcesses.filter(employeeID=employee.id).values('processID', 'quantity')
    # print(currCompletedProcesses)
    for currCompletedProcess in currCompletedProcesses:
      # print(currCompletedProcess)
      qty = currCompletedProcess['quantity']
      processPrice = Process.objects.get(id=currCompletedProcess['processID'])
      # print("Price", processPrice)
      pieceRate = pieceRate + (qty*getattr(processPrice, 'price'))
      # print("Piece rate Payment: ", pieceRate)

    try: 
      dailySalaryObj = DailySalary.objects.get(employeeID=getattr(employee, 'id'))
      dailySalary = getattr(dailySalaryObj, 'dailySalary')
    except:
      dailySalary = 0
    
    salaries.append(Salary(employee, dailySalary, pieceRate))
    i = i+1

  # print(salaries)
  flag   = True
  if not completedProcesses:
    flag=False

  total = 0
  for salary in salaries:
    total = total + salary.total

  # Del the session creates an error when the page is refreshed
  # del request.session['startDate']
  # del request.session['endDate']

  context = {
    'salaries':salaries,
    'flags':flag,
    'startDate': start,
    'endDate': end,
    'total': total
  }

  return render(request, 'salary/salaries.html', context)

def inputDateSalary_view(request):
  endDate = date.today()
  startDate = endDate - timedelta(days=5)
  form = GetDateForm(request.POST or None, initial={'endDate': endDate, 'startDate':startDate})

  # print(form)
  # print("Error: ", form.errors)
  # print("Non field err: ", form.non_field_errors)
  if form.is_valid():
    request.session['startDate'] = form['startDate'].value()
    request.session['endDate'] = form['endDate'].value()

    return redirect(salary_view)

  context = {
    'form':form,
  }
  return render(request, "salary/inputDate.html", context)



















#ATTENDANCE RELATED VIEWS
def attendance_view(request):
  attendances = Attendance.objects.all().order_by('-date')
  flag   = True
  if not attendances:
    flag=False

  context = {
    'attendances':attendances,
    'flags':flag
  }
  return render(request, 'attendance/attendance.html', context)

def attendance_create_view(request):
  employee_id = request.session.get("employee")
  start = request.session.get("startDate")
  end = request.session.get("endDate")

  start = datetime.strptime(start, "%Y-%m-%d")
  end = datetime.strptime(end, "%Y-%m-%d")
  
  delta = end-start
  # print("How many days?", delta.days)
  dateList = []
  days = delta.days+1
  for i in range(delta.days+1):
    dateList.append(start)
    start = start + timedelta(days=1)


  AttendanceFormSet = inlineformset_factory(Employee, Attendance, form=AttendanceForm, fields=("date", "percentage"), extra=days)
  # AttendanceFormSet = formset_factory(AttendanceForm, extra=delta.days+1, initial=[{'date':x} for x in dateList])

  employee = Employee.objects.get(id=employee_id)
  formset = AttendanceFormSet(queryset=Attendance.objects.none(), instance=employee, initial=[{'date':x} for x in dateList])
  # form = AttendanceForm(initial={'employeeID':employee})
  # employees = Employee.objects.all()

  if request.method == 'POST':
    # form = AttendanceForm(request.POST)
    formset = AttendanceFormSet(request.POST, instance=employee, initial=[{'date':x} for x in dateList])
    if formset.is_valid():
      formset.save()
      return redirect(attendance_view)

  context = {
    'formset':formset,
    'employee':employee,
  }
  return render(request, "attendance/attendance_create.html", context)

def attendance_edit_view(request, attendance_id):
  return edit(request, attendance_id, AttendanceForm, Attendance, redirect(request.GET.get("next")), 'attendance/attendance_edit.html')
  # form = DailySalaryForm(instance=DailySalary.objects.get(id=attendance_id))

  # if request.method == "POST":
  #     form = DailySalaryForm(request.POST, request.FILES, instance=DailySalary.objects.get(id=attendance_id))

  #     if form.is_valid():
  #         form.save()
  #         return redirect(attendance_view)

  # return render(request, 'attendance/attendance_edit.html', {
  #     "form": form
  # })

def attendance_delete_view(request):
  delete(request, Attendance)
  return  redirect(attendance_view)

def inputDateAttendance_view(request):
  form1 = ChooseEmployeeForm(request.POST or None)
  endDate = date.today()
  startDate = endDate - timedelta(days=5)
  form2 = GetDateForm(request.POST or None, initial={'endDate': endDate, 'startDate':startDate})

  # print(form)
  # print("Error: ", form.errors)
  # print("Non field err: ", form.non_field_errors)
  if form1.is_valid() and form2.is_valid():
    request.session['employee'] = form1['employeeID'].value()
    request.session['startDate'] = form2['startDate'].value()
    request.session['endDate'] = form2['endDate'].value()

    return redirect(attendance_create_view)

  context = {
    'form1':form1,
    'form2':form2
  }
  return render(request, "attendance/inputDate.html", context)

def attendance_of_employee_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  attendances = Attendance.objects.filter(employeeID=employee_id)

  if attendances:
    #There's at least one completedProcess
    flag=True
  else:
    flag=False
  
  context = {
    'attendances':attendances,
    'flags':flag,
    'employee':employee,
  }
  return render(request, "attendance/attendance_of_employee.html", context)

def attendance_employee_create_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  form1 = ChooseEmployeeForm(request.POST or None, initial={'employeeID':employee})
  endDate = date.today()
  startDate = endDate - timedelta(days=5)
  form2 = GetDateForm(request.POST or None, initial={'endDate': endDate, 'startDate':startDate})

  if form1.is_valid() and form2.is_valid():
    request.session['employee'] = form1['employeeID'].value()
    request.session['startDate'] = form2['startDate'].value()
    request.session['endDate'] = form2['endDate'].value()

    return redirect(attendance_create_view)

  context = {
    'form1':form1,
    'form2':form2
  }
  return render(request, "attendance/inputDate.html", context)
