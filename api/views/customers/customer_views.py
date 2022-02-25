from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from customers.models import Customer
from api.serializers import CustomerSerializer as CustomerSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr, randomint


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCustomer(request):
    user = request.user
    data = request.data

    try:

        # Create the customer
        customer = Customer.objects.create(
            customer_id=randomstr(),
            customer_number=randomint(),
        )

        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this customer'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCustomers(request):
    user = request.user
    data = request.data

    customers = Customer.objects.filter(
        status='active',
    ).order_by('-created_at')

    page = request.query_params.get('page')
    paginator = Paginator(customers, 5)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = CustomerSerializer(customers, many=True)
    return Response({'customers': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCustomer(request, customer_id):

    user = request.user

    # Check if the customer is valid
    customer = Customer.objects.filter(customer_id=customer_id, status='active').first()
    if not customer:
        message = {'detail': 'Customer does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateCustomer(request, customer_id):
    data = request.data
    user = request.user

    # Check if the customer is valid
    customer = Customer.objects.filter(customer_id=customer_id, status='active').first()
    if not customer:
        message = {'detail': 'Customer does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO add updates here
    
    serializer = CustomerSerializer(customer, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveCustomer(request, customer_id):
    
    user = request.user

    # Check if the customer is valid
    customer = Customer.objects.filter(customer_id=customer_id, status='active').first()
    if not customer:
        message = {'detail': 'Customer does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    customer.status = 'archived'
    customer.save()
    message = {'detail': 'Customer was archived'}
    return Response(message, status=200)     

  