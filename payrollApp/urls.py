from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name="home"),

    path('order/', views.order_view, name="order"),
    path('order/create/', views.order_create_view, name="create-order"),
    path('order/edit/<order_id>/', views.order_edit_view, name="edit-order"),
    path('order/delete/', views.order_delete_view, name="delete-order"),

    path('process/', views.process_view, name="process"),
    path('process/order/<order_id>/', views.process_of_order_view, name="process-of-order"),
    # path('process/order/<order_code>/', views.process_of_order_view, name="process-of-order"),
    path('process/create/', views.process_create_view, name="create-process"),
    path('process/create/<order_id>/', views.process_order_create_view, name="create-process"),
    path('process/edit/<process_id>/', views.process_edit_view, name="edit-process"),
    path('process/delete/', views.process_delete_view, name="delete-process"),

    path('employee/', views.employee_view, name="employee"),
    path('employee/create/', views.employee_create_view, name="create-employee"),
    path('employee/edit/<employee_id>/', views.employee_edit_view, name="edit-employee"),
    path('employee/delete/', views.employee_delete_view, name="delete-employee"),

    path('position/', views.position_view, name="position"),
    path('position/create/', views.position_create_view, name="create-position"),
    path('position/edit/<position_id>/', views.position_edit_view, name="edit-position"),
    path('position/delete/', views.position_delete_view, name="delete-position"),
    
    path('employmentType/', views.employmentType_view, name="employmentType"),
    path('employmentType/create/', views.employmentType_create_view, name="create-employmentType"),
    path('employmentType/edit/<employmentType_id>/', views.employmentType_edit_view, name="edit-employmentType"),
    path('employmentType/delete/', views.employmentType_delete_view, name="delete-employmentType"),

    path('completedProcess/', views.completedProcess_view, name="completedProcess"),
    path('completedProcess/process/<process_id>/', views.completedProcess_of_process_view, name="completedProcess-of-process"),
    path('completedProcess/employee/<employee_id>/', views.completedProcess_of_employee_view, name="completedProcess-of-employee"),
    path('completedProcess/create/', views.completedProcess_create_view, name="create-completedProcess"),
    path('completedProcess/create/<process_id>/', views.completedProcess_process_create_view, name="create-completedProcess"),
    path('completedProcess/employee/create/<employee_id>/', views.completedProcess_employee_create_view, name="create-completedProcess-employee"),
    path('completedProcess/edit/<completedProcess_id>/', views.completedProcess_edit_view, name="edit-completedProcess"),
    path('completedProcess/delete/', views.completedProcess_delete_view, name="delete-completedProcess"),

    path('dailySalary/', views.dailySalary_view, name="dailySalary"),
    path('dailySalary/create/', views.dailySalary_create_view, name="create-dailySalary"),
    path('dailySalary/edit/<dailySalary_id>/', views.dailySalary_edit_view, name="edit-dailySalary"),
    path('dailySalary/delete/', views.dailySalary_delete_view, name="delete-dailySalary"),

    path('salary/date', views.inputDateSalary_view, name="inputDate-salary"),
    path('salary/', views.salary_view, name="salary"),
    
    path('attendance/date', views.inputDateAttendance_view, name="inputDate-attendance"),
    path('attendance/', views.attendance_view, name="attendance"),
    path('attendance/create/', views.attendance_create_view, name="create-attendance"),
    path('attendance/edit/<attendance_id>/', views.attendance_edit_view, name="edit-attendance"),
    path('attendance/delete/', views.attendance_delete_view, name="delete-attendance"),
    path('attendance/employee/<employee_id>/', views.attendance_of_employee_view, name="attendance-of-employee"),
    path('attendance/employee/create/<employee_id>/', views.attendance_employee_create_view, name="create-attendance-employee"),

]