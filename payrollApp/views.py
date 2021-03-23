from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Order, Process, Employee, EmploymentType, Position
from .forms import OrderForm, ProcessForm, EmployeeForm, PositionForm, EmploymentTypeForm
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
  processes = Process.objects.filter(orderId=order_id)
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
#   processes = Process.objects.filter(orderId=order_code)
#   # processes = Process.objects.get(id=order_id)
#   if processes:
#     #There's at least one process
#     flag=True
#   else:
#     flag=False

#   context = {
#     'processes':processes,
#     'flags':flag,
#     'orderId':order_id,
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
  form.fields['orderId'].initial = order_id
  form.fields['orderId'].disabled = True
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