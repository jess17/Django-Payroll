from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name="home"),
    path('order/', views.order_view, name="order"),
    path('order/create/', views.order_create_view, name="create-order"),
    path('order/edit/<order_id>/', views.order_edit_view, name="edit-order"),

    path('process/', views.process_view, name="process"),
    path('process/order/<order_id>/', views.process_of_order_view, name="process-of-order"),
    # path('process/order/<order_code>/', views.process_of_order_view, name="process-of-order"),
    path('process/create/', views.process_create_view, name="create-process"),
    path('process/create/<order_id>/', views.process_order_create_view, name="create-process"),
    path('process/edit/<process_id>/', views.process_edit_view, name="edit-process"),

    path('employee/', views.employee_view, name="employee"),
    path('employee/create/', views.employee_create_view, name="create-employee"),
    path('employee/edit/<employee_id>/', views.employee_edit_view, name="edit-employee"),

    path('position/', views.position_view, name="position"),
    path('position/create/', views.position_create_view, name="create-position"),
    path('position/edit/<position_id>/', views.position_edit_view, name="edit-position"),
    
    path('employmentType/', views.employmentType_view, name="employmentType"),
    path('employmentType/create/', views.employmentType_create_view, name="create-employmentType"),
    path('employmentType/edit/<employmentType_id>/', views.employmentType_edit_view, name="edit-employmentType"),
]