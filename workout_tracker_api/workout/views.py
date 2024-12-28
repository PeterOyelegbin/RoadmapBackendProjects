from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from utils import general_logger
from .serializers import Exercise, ExerciseSerializer, Plan, PlanSerializer, Session, SessionSerializer


# Create your views here.
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (AllowAny,)

    def get_permissions(self):
        """
        Return the appropriate permissions based on the action.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def list(self, request, *args, **kwargs):
        try:
            objects = self.filter_queryset(self.get_queryset())
            if not objects:
                raise Exercise.DoesNotExist
            serializer = self.get_serializer(objects, many=True)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Exercise listed successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "No records found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ExerciseSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 201,
                "message": "Exercise created successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            instance = Exercise.objects.get(pk=pk)
            serializer = self.get_serializer(instance)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Exercise details retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Exercise does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=ExerciseSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = Exercise.objects.get(pk=pk)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 200,
                "message": "Exercise updated successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exercise.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Exercise does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ExerciseSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, partial=True, *args, **kwargs)

    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = Exercise.objects.get(pk=pk)
            instance.delete()
            response_data = {
                "success": True,
                "status": 204,
                "message": "Exercise deleted successfully",
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Exercise.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Exercise does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        

class PlanViewSet(viewsets.ViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Plan.objects.none()
        return Plan.objects.filter(user=self.request.user)

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def list(self, request, *args, **kwargs):
        try:
            objects = self.get_queryset()
            if not objects:
                raise Plan.DoesNotExist
            serializer = PlanSerializer(objects, many=True)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout plans listed successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Plan.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "No records found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=PlanSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST', 404: ''})
    def create(self, request, *args, **kwargs):
        serializer = PlanSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            exercise_id = serializer.validated_data['exercise_id']
            exercise = Exercise.objects.get(pk=exercise_id)
            user = request.user
            serializer.save(user=user, exercise=exercise)
            response_data = {
                "success": True,
                "status": 201,
                "message": "Workout plan created successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exercise.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Exercise does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            instance = Plan.objects.get(pk=pk)
            serializer = PlanSerializer(instance)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout plan details retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Plan.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout plan does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=PlanSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = Plan.objects.get(pk=pk)
            serializer = PlanSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout plan updated successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Plan.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout plan does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = Plan.objects.get(pk=pk)
            instance.delete()
            response_data = {
                "success": True,
                "status": 204,
                "message": "Workout plan deleted successfully",
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Plan.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout plan does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        

class SessionViewSet(viewsets.ViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Session.objects.none()
        return Session.objects.filter(user=self.request.user)

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def list(self, request, *args, **kwargs):
        try:
            objects = self.get_queryset()
            if not objects:
                raise Session.DoesNotExist
            serializer = SessionSerializer(objects, many=True)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout sessions listed successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "No records found",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=SessionSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST', 404: ''})
    def create(self, request, *args, **kwargs):
        serializer = SessionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            plan_id = serializer.validated_data['plan_id']
            plan = Plan.objects.get(pk=plan_id)
            user = request.user
            serializer.save(user=user, plan=plan)
            response_data = {
                "success": True,
                "status": 201,
                "message": "Workout session created successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Plan.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout plan does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT FOUND'})
    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            instance = Session.objects.get(pk=pk)
            serializer = SessionSerializer(instance)
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout session details retrieved successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout session does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(request_body=SessionSerializer, responses={200: 'OK', 400: 'BAD REQUEST', 404: 'NOT FOUND'})
    def update(self, request, pk=None, *args, **kwargs):
        try:
            instance = Session.objects.get(pk=pk)
            serializer = SessionSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "success": True,
                "status": 200,
                "message": "Workout session updated successfully",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout session does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                "success": False,
                "status": 400,
                "message": "Validation error: Invalid input from user or empty fields",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={204: 'NO CONTENT', 404: 'NOT FOUND'})
    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            instance = Session.objects.get(pk=pk)
            instance.delete()
            response_data = {
                "success": True,
                "status": 204,
                "message": "Workout session deleted successfully",
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist:
            response_data = {
                "success": False,
                "status": 404,
                "message": "Workout session does not exist",
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        