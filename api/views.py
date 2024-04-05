from rest_framework.views import APIView,Response,status
from . import serializers
from main.models import User
from django.contrib.auth.models import Group

class EmployeeRegView(APIView):
    def post(self,request):
        serializer = serializers.UserRegSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save(commit=False)
            employee.role = User.EMPLOYEE
            employee.is_active = False
            employee.save()
            group = Group.objects.get_or_create(name="Employee")
            group.user_set.add(employee)
            return Response({
                "status" : "success",
                "message" : serializer.data
            },status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                "status" : "failure",
                "message" : serializer.errors
            },status=status.HTTP_400_BAD_REQUEST
            )