from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from .models import Empleado, Departamento, Permiso, Rol

admin.site.register(Empleado)
admin.site.register(Departamento)
admin.site.register(Permiso)
admin.site.register(Rol)

# Asignar permisos al grupo de Recursos Humanos
group_hr, created = Group.objects.get_or_create(name='Recursos Humanos')
if created:
    change_salary_permission = Permission.objects.get(codename='change_salary')
    change_position_permission = Permission.objects.get(codename='change_position')
    group_hr.permissions.add(change_salary_permission, change_position_permission)



