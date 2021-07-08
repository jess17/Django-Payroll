from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.core.exceptions import ValidationError


# from django.urls import reverse
from datetime import date, datetime, timedelta

from django.forms import inlineformset_factory
from django.forms import formset_factory

from .models import Order, Process, Employee, EmploymentType, Position, CompletedProcess, DailySalary, Attendance, Allowance, Deduction
from .forms import UserForm, OrderForm, ProcessForm, EmployeeForm, PositionForm, EmploymentTypeForm, CompletedProcessForm, DailySalaryForm, GetDateForm, AttendanceForm, ChooseEmployeeForm, AllowanceForm, DeductionForm
from .filters import OrderFilter, AllowanceFilter, DeductionFilter, EmployeeFilter, CompletedProcessFilter, ProcessFilter, AttendanceFilter, AttendanceOfEmployeeFilter, CompletedProcessOfProcessFilter, CompletedProcessOfEmployeeFilter, ProcessOfOrderFilter

#IMPORT FOR PDF
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    return redirect(employee_view)

def create(request, Form, redirectVal, returnLoc):
  form = Form(request.POST or None)
  if form.is_valid():
    form.save()
    return redirectVal

  context = {
    'form':form
  }
  return render(request, returnLoc, context)

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
@login_required(login_url='login')
def order_view(request):
  orders = Order.objects.all().order_by('-lastModified')
  flag   = True
  if not orders:
    flag=False
  
  myFilter = OrderFilter(request.GET, queryset=orders)
  orders = myFilter.qs

  context = {
    'orders':orders,
    'flags': flag,
    'myFilter': myFilter
  }
  return render(request, "order/order.html", context)

@login_required(login_url='login')
def order_create_view(request):
    return create(request, OrderForm, redirect(order_view), 'order/order_create.html')

@login_required(login_url='login')
def order_edit_view(request, order_id):
  return edit(request, order_id, OrderForm, Order, redirect(request.GET.get("next")), 'order/order_edit.html')

@login_required(login_url='login')
def order_delete_view(request):
  delete(request, Order)
  return redirect(request.GET.get("next"))








#PROCESS RELATED VIEWS
@login_required(login_url='login')
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

  myFilter = ProcessFilter(request.GET, queryset=processes)
  processes = myFilter.qs

  context = {
    'processes':processes,
    'orderFlag':orderFlag,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, "process/process.html", context)

@login_required(login_url='login')
def process_of_order_view(request, order_id):
  order = Order.objects.get(id=order_id)
  processes = Process.objects.filter(orderID=order_id)

  if processes:
    #There's at least one process
    flag=True
  else:
    flag=False
  
  myFilter = ProcessOfOrderFilter(request.GET, queryset=processes)
  processes = myFilter.qs

  context = {
    'processes':processes,
    'flags':flag,
    'order':order,
    'myFilter': myFilter
  }
  return render(request, "process/process_of_order.html", context)


@login_required(login_url='login')
def process_create_view(request):
  return create(request, ProcessForm, redirect(request.GET.get("next")), 'process/process_create.html')

@login_required(login_url='login')
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

@login_required(login_url='login')
def process_edit_view(request, process_id):
  form = ProcessForm(instance=Process.objects.get(id=process_id))

  if request.method == "POST":
    form = ProcessForm(request.POST, request.FILES, instance=Process.objects.get(id=process_id), id=process_id)

    if form.is_valid():
        form.save()
        return redirect(request.GET.get("next"))

  return render(request, 'process/process_edit.html', {
      "form": form,
  })

@login_required(login_url='login')
def process_delete_view(request):
  delete(request, Process)
  return redirect(request.GET.get("next"))







#EMPLOYEE RELATED VIEWS
@login_required(login_url='login')
def employee_view(request):
  employees = Employee.objects.all()
  flag   = True
  if not employees:
    flag=False

  myFilter = EmployeeFilter(request.GET, queryset=employees)
  employees = myFilter.qs

  context = {
    'employees':employees,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, 'employee/employee.html', context)

@login_required(login_url='login')
def employee_create_view(request):
  form = EmployeeForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect(employee_view)

  context = {
    'form':form,
  }
  return render(request, "employee/employee_create.html", context)

@login_required(login_url='login')
def employee_edit_view(request, employee_id):
  return edit(request, employee_id, EmployeeForm, Employee, redirect(request.GET.get("next")), 'employee/employee_edit.html')

@login_required(login_url='login')
def employee_delete_view(request):
  delete(request, Employee)
  return redirect(employee_view)











#POSITION RELATED VIEWS
@login_required(login_url='login')
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

@login_required(login_url='login')
def position_create_view(request):
  return create(request, PositionForm, redirect(request.GET.get("next")), 'employee/position/position_create.html')

@login_required(login_url='login')
def position_edit_view(request, position_id):
  return edit(request, position_id, PositionForm, Position, redirect(request.GET.get("next")), 'employee/position/position_edit.html')

@login_required(login_url='login')
def position_delete_view(request):
  delete(request, Position)
  return redirect(position_view)











#EMPLOYMENT TYPE RELATED VIEWS
@login_required(login_url='login')
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

@login_required(login_url='login')
def employmentType_create_view(request):
  return create(request, EmploymentTypeForm, redirect(request.GET.get("next")), 'employee/employmentType/employmentType_create.html')

@login_required(login_url='login')
def employmentType_edit_view(request, employmentType_id):
  return edit(request, employmentType_id, EmploymentTypeForm, EmploymentType, redirect(request.GET.get("next")), 'employee/employmentType/employmentType_edit.html')

@login_required(login_url='login')
def employmentType_delete_view(request):
  delete(request, EmploymentType)
  return redirect(employmentType_view)












#COMPLETED PROCESS RELATED VIEWS
@login_required(login_url='login')
def completedProcess_view(request):
  completedProcesses = CompletedProcess.objects.all().order_by('-id')

  flag   = True
  if not completedProcesses:
    flag=False

  processes = Process.objects.exists()
  processFlag=True
  if not processes:
    processFlag=False

  myFilter = CompletedProcessFilter(request.GET, queryset=completedProcesses)
  completedProcesses = myFilter.qs

  context = {
    'completedProcesses':completedProcesses,
    'processFlag':processFlag,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, "completedProcess/completedProcess.html", context)

@login_required(login_url='login')
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
  
  myFilter = CompletedProcessOfProcessFilter(request.GET, queryset=completedProcesses)
  completedProcesses = myFilter.qs

  context = {
    'completedProcesses':completedProcesses,
    'flags':flag,
    'process':process,
    'completedQty':completedQty,
    'myFilter': myFilter
  }
  return render(request, "completedProcess/completedProcess_of_process.html", context)

@login_required(login_url='login')
def completedProcess_of_employee_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  completedProcesses = CompletedProcess.objects.filter(employeeID=employee_id).order_by('-dateRecorded')

  if completedProcesses:
    #There's at least one completedProcess
    flag=True
  else:
    flag=False
  
  myFilter = CompletedProcessOfEmployeeFilter(request.GET, queryset=completedProcesses)
  completedProcesses = myFilter.qs

  context = {
    'completedProcesses':completedProcesses,
    'flags':flag,
    'employee':employee,
    'myFilter': myFilter
  }
  return render(request, "completedProcess/completedProcess_of_employee.html", context)

@login_required(login_url='login')
def completedProcess_create_view(request):
  return create(request, CompletedProcessForm, redirect(request.GET.get("next")), 'completedProcess/completedProcess_create.html')

@login_required(login_url='login')
def completedProcess_process_create_view(request, process_id):
  form = CompletedProcessForm(request.POST or None)
  form.fields['processID'].initial = process_id
  form.fields['processID'].disabled = True
  process = Process.objects.get(id=process_id)


  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form,

  }
  return render(request, "completedProcess/completedProcess_create.html", context)

@login_required(login_url='login')
def completedProcess_employee_create_view(request, employee_id):
  form = CompletedProcessForm(request.POST or None)
  form.fields['employeeID'].initial = employee_id
  form.fields['employeeID'].disabled = True
 
  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "completedProcess/completedProcess_create.html", context)

@login_required(login_url='login')
def completedProcess_edit_view(request, completedProcess_id):
  return edit(request, completedProcess_id, CompletedProcessForm, CompletedProcess, redirect(request.GET.get("next")), 'completedProcess/completedProcess_edit.html')

@login_required(login_url='login')
def completedProcess_delete_view(request):
  delete(request, CompletedProcess)
  return redirect(request.GET.get("next"))












#DAILY SALARY RELATED VIEWS
@login_required(login_url='login')
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

@login_required(login_url='login')
def dailySalary_create_view(request):
  return create(request, DailySalaryForm, redirect(dailySalary_view), 'salary/dailySalary_create.html')

@login_required(login_url='login')
def dailySalary_edit_view(request, dailySalary_id):
  return edit(request, dailySalary_id, DailySalaryForm, DailySalary, redirect(dailySalary_view), 'salary/dailySalary_edit.html')

@login_required(login_url='login')
def dailySalary_delete_view(request):
  delete(request, DailySalary)
  return  redirect(dailySalary_view)















#SALARY RELATED VIEWS
class Salary:
  def __init__(self, employeeID, salary, pieceRate, allowance, deduction):
    self.employeeID = employeeID
    self.salary = salary
    self.pieceRate = pieceRate
    self.allowance = allowance
    self.deduction = deduction
    self.total = float(salary)+float(pieceRate)+float(allowance)-float(deduction)

  def getSalary(self, employeeID):
    return {'salary': self.salary, 'allowance':self.allowance, 'deduction':self.deduction, 'total':self.total}

def getSalary(request):
  start = request.session.get("startDate")
  end = request.session.get("endDate")

  endPlus1 = datetime.strptime(end, "%Y-%m-%d")
  endPlus1 = endPlus1 + timedelta(days=1)
  completedProcesses = CompletedProcess.objects.filter(dateRecorded__range=[start, endPlus1])
  employees          = Employee.objects.all().exclude(terminationDate__isnull=False) #exclude employee that has been terminated
  attendances        = Attendance.objects.filter(date__range=[start, endPlus1])
  allowance          = Allowance.objects.filter(date__range=[start, endPlus1])
  deduction          = Deduction.objects.filter(date__range=[start, endPlus1])
  
  salaries = []
  i = 0
  for employee in employees:
    pieceRate = 0
    currCompletedProcesses = completedProcesses.filter(employeeID=employee.id).values('processID', 'quantity')
    for currCompletedProcess in currCompletedProcesses:
      qty = currCompletedProcess['quantity']
      processPrice = Process.objects.get(id=currCompletedProcess['processID'])
      pieceRate = pieceRate + (qty*getattr(processPrice, 'price'))
    
    currAttendances = attendances.filter(employeeID=employee.id).values('percentage')
    attendancePercentage = 0
    for i in range(len(currAttendances)):
      currPercentage = currAttendances[i]['percentage']
      attendancePercentage = attendancePercentage + currPercentage
    if attendancePercentage > 0:
      attendancePercentage = attendancePercentage/100

    try: 
      dailySalaryObj = DailySalary.objects.get(employeeID=getattr(employee, 'id'))
      salary = float(getattr(dailySalaryObj, 'dailySalary'))*attendancePercentage

    except:
      salary = 0
    
    currAllowances = allowance.filter(employeeID=employee.id).values('amount')
    allowanceAmt = 0
    for i in range(len(currAllowances)):
      currAmt = currAllowances[i]['amount']
      allowanceAmt = allowanceAmt + currAmt

    currDeductions = deduction.filter(employeeID=employee.id).values('amount')
    deductionAmt = 0
    for i in range(len(currDeductions)):
      currAmt = currDeductions[i]['amount']
      deductionAmt = deductionAmt + currAmt

    salaries.append(Salary(employee, salary, pieceRate, allowanceAmt, deductionAmt))
    i = i+1

  flag   = True
  if not completedProcesses and not attendances and not allowance and not deduction:
    flag=False

  total = 0
  for salary in salaries:
    total = total + salary.total

  context = {
    'salaries':salaries,
    'flags':flag,
    'startDate': start,
    'endDate': end,
    'total': total
  }
  return context

@login_required(login_url='login')
def salary_view(request):
  context = getSalary(request)
  return render(request, 'salary/salaries.html', context)

@login_required(login_url='login')
def inputDateSalary_view(request):
  endDate = date.today()
  startDate = endDate - timedelta(days=5)
  form = GetDateForm(request.POST or None, initial={'endDate': endDate, 'startDate':startDate})

  if form.is_valid():
    request.session['startDate'] = form['startDate'].value()
    request.session['endDate'] = form['endDate'].value()

    return redirect(salary_view)

  context = {
    'form':form,
  }
  return render(request, "salary/inputDate.html", context)

def getSalaryOfEmployeeDetails(request, employee_id):
  start = request.session.get("startDate")
  end = request.session.get("endDate")

  endPlus1 = datetime.strptime(end, "%Y-%m-%d")
  endPlus1 = endPlus1 + timedelta(days=1)
  completedProcesses = CompletedProcess.objects.filter(dateRecorded__range=[start, endPlus1])
  employee           = Employee.objects.get(id=employee_id)
  attendances        = Attendance.objects.filter(date__range=[start, endPlus1])
  allowance          = Allowance.objects.filter(date__range=[start, endPlus1])
  deduction          = Deduction.objects.filter(date__range=[start, endPlus1])
  
  salaryDetails = {}
  totalPieceRatePayment = 0
  completedProcesses = completedProcesses.filter(employeeID=employee_id).values('processID', 'quantity')
  completedProcessList = []

  for completedProcess in completedProcesses:
    qty = completedProcess['quantity']
    currProcess = Process.objects.get(id=completedProcess['processID'])
    processName = getattr(currProcess, 'name')
    price = getattr(currProcess, 'price')
    currPieceRatePayment = (qty*price)
    totalPieceRatePayment = totalPieceRatePayment + currPieceRatePayment
    currOrderID = getattr(currProcess, 'orderID')
    currOrderCode = Order.objects.get(id=getattr(currOrderID, 'id'))
    orderCode = getattr(currOrderCode, 'code')

    completedProcessList.append([orderCode, processName, qty, price, currPieceRatePayment])

  salaryDetails['pieceRateDetails'] = completedProcessList
  
  currAttendances = attendances.filter(employeeID=employee_id).values('percentage')
  attendancePercentage = 0
  for i in range(len(currAttendances)):
    currPercentage = currAttendances[i]['percentage']
    attendancePercentage = attendancePercentage + currPercentage
  if attendancePercentage > 0:
    attendancePercentage = attendancePercentage/100
  

  try: 
    dailySalaryObj = DailySalary.objects.get(employeeID=employee_id)
    salary = float(getattr(dailySalaryObj, 'dailySalary'))*attendancePercentage

  except:
    salary = 0
  

  currAllowances = allowance.filter(employeeID=employee_id).values('amount')
  allowanceAmt = 0
  for i in range(len(currAllowances)):
    currAmt = currAllowances[i]['amount']
    allowanceAmt = allowanceAmt + currAmt

  

  currDeductions = deduction.filter(employeeID=employee_id).values('amount')
  deductionAmt = 0
  for i in range(len(currDeductions)):
    currAmt = currDeductions[i]['amount']
    deductionAmt = deductionAmt + currAmt

  flag   = True
  if not completedProcessList:
    flag=False

  total = float(totalPieceRatePayment) + salary + float(allowanceAmt) - float(deductionAmt)

  context = {
    'flags':flag,
    'employee': employee,
    'startDate': start,
    'endDate': end,
    'attendance': attendancePercentage,
    'totalPieceRatePayment': totalPieceRatePayment,
    'salary': salary,
    'allowance': allowanceAmt,
    'deduction': deductionAmt,
    'total': total,
    'completedProcessList':completedProcessList
  }

  return context

@login_required(login_url='login')
def salary_of_employee_details_view(request, employee_id):
  request.session['employee_id'] = employee_id
  context = getSalaryOfEmployeeDetails(request, employee_id)
  return render(request, 'salary/salary_of_employee_details.html', context)


















#ATTENDANCE RELATED VIEWS
@login_required(login_url='login')
def attendance_view(request):
  attendances = Attendance.objects.all().order_by('-date')
  flag   = True
  if not attendances:
    flag=False

  myFilter = AttendanceFilter(request.GET, queryset=attendances)
  attendances = myFilter.qs

  context = {
    'attendances':attendances,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, 'attendance/attendance.html', context)

@login_required(login_url='login')
def attendance_create_view(request):
  employee_id = request.session.get("employee")
  start = request.session.get("startDate")
  end = request.session.get("endDate")

  start = datetime.strptime(start, "%Y-%m-%d")
  end = datetime.strptime(end, "%Y-%m-%d")
  
  delta = end-start
  dateList = []
  days = delta.days+1
  for i in range(delta.days+1):
    dateList.append(start)
    start = start + timedelta(days=1)


  AttendanceFormSet = inlineformset_factory(Employee, Attendance, form=AttendanceForm, fields=("date", "percentage"), extra=days)

  employee = Employee.objects.get(id=employee_id)
  formset = AttendanceFormSet(queryset=Attendance.objects.none(), instance=employee, initial=[{'date':x} for x in dateList])

  if request.method == 'POST':
    formset = AttendanceFormSet(request.POST, instance=employee, initial=[{'date':x} for x in dateList])
    if formset.is_valid():
      formset.save()
      return redirect(attendance_view)

  context = {
    'formset':formset,
    'employee':employee,
  }
  return render(request, "attendance/attendance_create.html", context)

@login_required(login_url='login')
def attendance_edit_view(request, attendance_id):
  return edit(request, attendance_id, AttendanceForm, Attendance, redirect(request.GET.get("next")), 'attendance/attendance_edit.html')

@login_required(login_url='login')
def attendance_delete_view(request):
  delete(request, Attendance)
  return  redirect(request.GET.get("next"))

@login_required(login_url='login')
def inputDateAttendance_view(request):
  form1 = ChooseEmployeeForm(request.POST or None)
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

@login_required(login_url='login')
def attendance_of_employee_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  attendances = Attendance.objects.filter(employeeID=employee_id)

  if attendances:
    flag=True
  else:
    flag=False
  
  myFilter = AttendanceOfEmployeeFilter(request.GET, queryset=attendances)
  attendances = myFilter.qs

  context = {
    'attendances':attendances,
    'flags':flag,
    'employee':employee,
    'myFilter': myFilter
  }
  return render(request, "attendance/attendance_of_employee.html", context)

@login_required(login_url='login')
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













#ALLOWANCE RELATED VIEWS
@login_required(login_url='login')
def allowance_view(request):
  allowances = Allowance.objects.all()

  flag   = True
  if not allowances:
    flag=False

  myFilter = AllowanceFilter(request.GET, queryset=allowances)
  allowances = myFilter.qs

  context = {
    'allowances':allowances,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, 'salary/allowance/allowance.html', context)

@login_required(login_url='login')
def allowance_create_view(request):
  return create(request, AllowanceForm, redirect(allowance_view), 'salary/allowance/allowance_create.html')

@login_required(login_url='login')
def allowance_edit_view(request, allowance_id):
  return edit(request, allowance_id, AllowanceForm, Allowance, redirect(request.GET.get("next")), 'salary/allowance/allowance_edit.html')

@login_required(login_url='login')
def allowance_delete_view(request):
  delete(request, Allowance)
  return  redirect(request.GET.get("next"))











#DEDUCTION RELATED VIEWS
@login_required(login_url='login')
def deduction_view(request):
  deductions = Deduction.objects.all()

  flag   = True
  if not deductions:
    flag=False

  myFilter = DeductionFilter(request.GET, queryset=deductions)
  deductions = myFilter.qs

  context = {
    'deductions':deductions,
    'flags':flag,
    'myFilter':myFilter
  }
  return render(request, 'salary/deduction/deduction.html', context)

@login_required(login_url='login')
def deduction_create_view(request):
  return create(request, DeductionForm, redirect(deduction_view), 'salary/deduction/deduction_create.html')

@login_required(login_url='login')
def deduction_edit_view(request, deduction_id):
  return edit(request, deduction_id, DeductionForm, Deduction, redirect(request.GET.get("next")), 'salary/deduction/deduction_edit.html')

@login_required(login_url='login')
def deduction_delete_view(request):
  delete(request, Deduction)
  return  redirect(request.GET.get("next"))














#TO PDF RELATED VIEWS
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

#Opens up page as PDF
class ViewSalaryPDF(View):
  def get(self, request, *args, **kwargs):
    data = getSalary(request)
    
    pdf = render_to_pdf('salary/salaries_pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


#Automatically downloads to PDF file
class DownloadSalaryPDF(View):
  def get(self, request, *args, **kwargs):
    data = getSalary(request)
    pdf = render_to_pdf('salary/salaries_pdf_template.html', data)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Salary_%s_to_%s.pdf" %(data["startDate"], data["endDate"])
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response

class ViewSalaryOfEmployeeDetailsPDF(View):
  def get(self, request, *args, **kwargs):
    employee_id = request.session.get("employee_id")
    data = getSalaryOfEmployeeDetails(request, employee_id)

    pdf = render_to_pdf('salary/salary_of_employee_details_pdf_template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

class DownloadSalaryOfEmployeeDetailsPDF(View):
  def get(self, request, *args, **kwargs):
    employee_id = request.session.get("employee_id")
    data = getSalaryOfEmployeeDetails(request, employee_id)
    pdf = render_to_pdf('salary/salary_of_employee_details_pdf_template.html', data)
    
    employee = data["employee"]
    employeeName = str(employee).split("|")[1]

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Salary_details_of_%s_%s_to_%s.pdf" %(employeeName, data["startDate"], data["endDate"])
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response
