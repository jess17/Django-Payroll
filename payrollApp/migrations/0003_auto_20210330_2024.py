# Generated by Django 3.1.7 on 2021-03-30 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payrollApp', '0002_auto_20210330_1817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='completedprocess',
            old_name='employeeId',
            new_name='employeeID',
        ),
        migrations.RenameField(
            model_name='completedprocess',
            old_name='processId',
            new_name='processID',
        ),
    ]
