
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Empleado, Departamento, Permiso, Rol
from .serializers import EmpleadoSerializer, DepartamentoSerializer, PermisoSerializer, RolSerializer
from .forms import EmpleadoForm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class MyView(APIView):
    @swagger_auto_schema(
        operation_summary="Resumen de la operación",
        operation_description="Descripción detallada de la operación",
        responses={200: "Respuesta exitosa"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['username', 'password']
        )
    )
    def post(self, request):
        # Lógica de la vista
        return Response({"message": "Operación exitosa"}, status=200)
    
# Funciones de autenticación
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'mensaje': 'Inicio de sesión exitoso'}, status=200)
        else:
            return JsonResponse({'mensaje': 'Credenciales inválidas'}, status=400)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'mensaje': 'Cierre de sesión exitoso'}, status=200)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def actualizar_salario(self, request, pk=None):
        empleado = self.get_object()
        if request.user.has_perm('gestion_de_nomina.change_salary'):
            empleado.salario = request.data.get('salario')
            empleado.save()
            return Response({'status': 'salario actualizado'})
        else:
            return Response({'status': 'no tiene permiso para actualizar el salario'}, status=403)

    @action(detail=True, methods=['post'])
    def actualizar_cargo(self, request, pk=None):
        empleado = self.get_object()
        if request.user.has_perm('gestion_de_nomina.change_position'):
            empleado.cargo = request.data.get('cargo')
            empleado.save()
            return Response({'status': 'cargo actualizado'})
        else:
            return Response({'status': 'no tiene permiso para actualizar el cargo'}, status=403)

    @action(detail=False, methods=['get'])
    def listar_empleados(self, request):
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def crear_empleado(self, request):
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Empleado creado correctamente'}, status=201)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get'])
    def ver_empleado(self, request, pk=None):
        empleado = get_object_or_404(Empleado, pk=pk)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def actualizar_empleado(self, request, pk=None):
        empleado = get_object_or_404(Empleado, pk=pk)
        serializer = EmpleadoSerializer(empleado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Empleado actualizado correctamente'}, status=200)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def eliminar_empleado(self, request, pk=None):
        empleado = get_object_or_404(Empleado, pk=pk)
        empleado.delete()
        return Response({'message': 'Empleado eliminado correctamente'}, status=200)

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializer
    permission_classes = [permissions.IsAuthenticated]

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]




