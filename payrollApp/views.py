from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Order, Process, Employee, EmploymentType, Position, CompletedProcess
from .forms import OrderForm, ProcessForm, EmployeeForm, PositionForm, EmploymentTypeForm, CompletedProcessForm
# Create your views here.
def home_view(request):
    return render(request, "real_base.html", {})


#ORDER RELATED VIEWS
def order_view(request):
  orders = Order.objects.all()
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
    form = OrderForm(instance=Order.objects.get(id=order_id))

    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=Order.objects.get(id=order_id))

        if form.is_valid():
            form.save()
            
            return redirect(order_view)

    return render(request, 'order/order_edit.html', {
        "form": form
    })

def order_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      for i in idList:
        Order.objects.get(id=i).delete()
      if idList:
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
    return redirect(order_view)








#PROCESS RELATED VIEWS
def process_view(request):
  processes = Process.objects.all()
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
  print(request)
  # processes = Process.objects.get(id=order_id)
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
    form = ProcessForm(instance=Process.objects.get(id=process_id))

    if request.method == "POST":
        form = ProcessForm(request.POST, request.FILES, instance=Process.objects.get(id=process_id))

        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return redirect(request.GET.get("next"))

    return render(request, 'process/process_edit.html', {
        "form": form
    })

def process_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      for i in idList:
        Process.objects.get(id=i).delete()
      if idList:
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
    return redirect(process_view)







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
  positions = Position.objects.all()
  employmentTypes = EmploymentType.objects.all()

  if form.is_valid():
    form.save()
    return redirect(employee_view)

  context = {
    'form':form,
    'positions': positions,
    'employmentTypes': employmentTypes
  }
  return render(request, "employee/employee_create.html", context)

def employee_edit_view(request, employee_id):
    form = EmployeeForm(instance=Employee.objects.get(id=employee_id))

    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=Employee.objects.get(id=employee_id))

        if form.is_valid():
            form.save()
            return redirect(employee_view)

    return render(request, 'employee/employee_edit.html', {
        "form": form
    })

def employee_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      for i in idList:
        Employee.objects.get(id=i).delete()
      if idList:
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
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
    form = PositionForm(instance=Position.objects.get(id=position_id))

    if request.method == "POST":
        form = PositionForm(request.POST, request.FILES, instance=Position.objects.get(id=position_id))

        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))

    return render(request, 'employee/position/position_edit.html', {
        "form": form
    })

def position_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      # print("idList", idList)
      for i in idList:
        # print(i)
        Position.objects.get(id=i).delete()
      if idList:
        # print("Something is inside of idList")
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
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
    form = EmploymentTypeForm(instance=EmploymentType.objects.get(id=employmentType_id))

    if request.method == "POST":
        form = EmploymentTypeForm(request.POST, request.FILES, instance=EmploymentType.objects.get(id=employmentType_id))

        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))

    return render(request, 'employee/employmentType/employmentType_edit.html', {
        "form": form
    })

def employmentType_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      for i in idList:
        EmploymentType.objects.get(id=i).delete()
      if idList:
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
    return redirect(employmentType_view)












#COMPLETED PROCESS RELATED VIEWS
def completedProcess_view(request):
  completedProcesses = CompletedProcess.objects.all()
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
  completedProcesses = CompletedProcess.objects.filter(processID=process_id)
  # print(request)

  if completedProcesses:
    #There's at least one completedProcess
    flag=True
  else:
    flag=False
  
  context = {
    'completedProcesses':completedProcesses,
    'flags':flag,
    'process':process,
  }
  return render(request, "completedProcess/completedProcess_of_process.html", context)

def completedProcess_of_employee_view(request, employee_id):
  employee = Employee.objects.get(id=employee_id)
  completedProcesses = CompletedProcess.objects.filter(employeeID=employee_id)

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
    'form':form
  }
  return render(request, "completedProcess/completedProcess_create.html", context)

def completedProcess_employee_create_view(request, employee_id):
  form = CompletedProcessForm(request.POST or None)
  form.fields['employeeID'].initial = employee_id
  form.fields['employeeID'].disabled = True
  employee = Employee.objects.get(id=employee_id)
  # form.fields['quantity'].initial = process.quantity


  if form.is_valid():
    form.save()
    return redirect(request.GET.get("next"))

  context = {
    'form':form
  }
  return render(request, "completedProcess/completedProcess_create.html", context)

def completedProcess_edit_view(request, completedProcess_id):
    form = CompletedProcessForm(instance=CompletedProcess.objects.get(id=completedProcess_id))

    if request.method == "POST":
        form = CompletedProcessForm(request.POST, request.FILES, instance=CompletedProcess.objects.get(id=completedProcess_id))
        
        # errMsg = "Quantity can't be greater than " + str(maxVal)
        # raise ValidationError(errMsg)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return redirect(request.GET.get("next"))

    return render(request, 'completedProcess/completedProcess_edit.html', {
        "form": form
    })

def completedProcess_delete_view(request, id=None):
    if request.method == "POST":
      idList = request.POST.getlist("selected")
      for i in idList:
        CompletedProcess.objects.get(id=i).delete()
      if idList:
        messages.success(request, "Selected rows has been successfully deleted")
      else:
        messages.info(request, "Nothing is selected")
    return redirect(completedProcess_view)