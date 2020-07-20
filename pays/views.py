from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from pays.serializers import UserSerializer, TransferSerializer, \
    FillUpSerializer
from pays.models import TransferTransaction, FillUpTransaction


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated,]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class Transaction(viewsets.ModelViewSet):
    serializer_class = None
    parser_classes = [JSONParser]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Transfer(Transaction):
    queryset = TransferTransaction.objects.all().order_by('-create_at')
    serializer_class = TransferSerializer


class FillUp(Transaction):
    queryset = FillUpTransaction.objects.all().order_by('-create_at')
    serializer_class = FillUpSerializer
