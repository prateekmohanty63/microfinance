from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loans.models import Product, ProductConfig, PaymentConfig
from api.serializers import LoanPaymentConfigSerializer as PaymentConfigSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPaymentConfig(request, product_id, product_config_id):
    user = request.user
    data = request.data

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product_config.product != product:
        message = {'detail': 'Product id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be looking at and editing product details (must be part of the org and admin)
    organization_id = product.organization.organization_id
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product.organization != user_organization['organization']:
        message = {'detail': 'Organization id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    try:

        # Create the product configuration
        payment_config = PaymentConfig.objects.create(
            payment_config_id=randomstr(),
            product_config=product_config,
            day=data['day'],
            structure=data['structure'],
            created_user=user,
        )

        if 'amount' in data:
            payment_config.amount=data['amount']
            payment_config.save()
        if 'label' in data:
            payment_config.label=data['label']
            payment_config.save()

        serializer = PaymentConfigSerializer(payment_config, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this payment configuration'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPaymentConfigs(request, product_id, product_config_id):
    user = request.user
    data = request.data

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product_config.product != product:
        message = {'detail': 'Product id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be looking at and editing product details (must be part of the org and admin)
    organization_id = product.organization.organization_id
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product.organization != user_organization['organization']:
        message = {'detail': 'Organization id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    organization = user_organization['organization']
    
    payment_configs = PaymentConfig.objects.filter(
        product_config=product_config,
        status='active',
    ).order_by('day')

    page = request.query_params.get('page')
    paginator = Paginator(payment_configs, 5)

    try:
        payment_configs = paginator.page(page)
    except PageNotAnInteger:
        payment_configs = paginator.page(1)
    except EmptyPage:
        payment_configs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = PaymentConfigSerializer(payment_configs, many=True)
    return Response({'payment_configs': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPaymentConfig(request, product_id, product_config_id, payment_config_id):

    user = request.user

    # Check to make sure the payment_config is valid
    payment_config = PaymentConfig.objects.filter(payment_config_id=payment_config_id, status='active').first()
    if not payment_config:
        message = {'detail': 'Payment configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product_config.product != product:
        message = {'detail': 'Product id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be looking at and editing product details (must be part of the org and admin)
    organization_id = product.organization.organization_id
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product.organization != user_organization['organization']:
        message = {'detail': 'Organization id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = PaymentConfigSerializer(payment_config, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePaymentConfig(request, product_id, product_config_id, payment_config_id):
    data = request.data
    user = request.user

    # Check to make sure the payment_config is valid
    payment_config = PaymentConfig.objects.filter(payment_config_id=payment_config_id, status='active').first()
    if not payment_config:
        message = {'detail': 'Payment configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product_config.product != product:
        message = {'detail': 'Product id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be looking at and editing product details (must be part of the org and admin)
    organization_id = product.organization.organization_id
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product.organization != user_organization['organization']:
        message = {'detail': 'Organization id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    if 'label' in data:   
        payment_config.label=data['label']
    if 'day' in data:
        payment_config.day=data['day']
    if 'structure' in data:
        payment_config.structure=data['structure']
    if 'amount' in data:
        payment_config.amount=data['amount']

    payment_config.save()
    serializer = PaymentConfigSerializer(payment_config, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archivePaymentConfig(request, product_id, product_config_id, payment_config_id):
    
    user = request.user

    # Check to make sure the payment_config is valid
    payment_config = PaymentConfig.objects.filter(payment_config_id=payment_config_id, status='active').first()
    if not payment_config:
        message = {'detail': 'Payment configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product_config.product != product:
        message = {'detail': 'Product id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be looking at and editing product details (must be part of the org and admin)
    organization_id = product.organization.organization_id
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if product.organization != user_organization['organization']:
        message = {'detail': 'Organization id is not valid'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    payment_config.status = 'archived'
    payment_config.save()
    message = {'detail': 'Payment configuration was archived'}
    return Response(message, status=200)     

  