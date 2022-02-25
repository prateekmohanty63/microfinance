from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loans.models import Product, ProductConfig, FeeConfig
from api.serializers import LoanFeeConfigSerializer as FeeConfigSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createFeeConfig(request, product_id, product_config_id):
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
        fee_config = FeeConfig.objects.create(
            fee_config_id=randomstr(),
            product_config=product_config,
            day=data['day'],
            structure=data['structure'],
            created_user=user,
        )

        if 'amount' in data:
            fee_config.amount=data['amount']
            fee_config.save()
        if 'label' in data:
            fee_config.label=data['label']
            fee_config.save()

        serializer = FeeConfigSerializer(fee_config, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this fee configuration'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFeeConfigs(request, product_id, product_config_id):
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
    
    fee_configs = FeeConfig.objects.filter(
        product_config=product_config,
        status='active',
    ).order_by('day')

    page = request.query_params.get('page')
    paginator = Paginator(fee_configs, 5)

    try:
        fee_configs = paginator.page(page)
    except PageNotAnInteger:
        fee_configs = paginator.page(1)
    except EmptyPage:
        fee_configs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = FeeConfigSerializer(fee_configs, many=True)
    return Response({'fee_configs': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFeeConfig(request, product_id, product_config_id, fee_config_id):

    user = request.user

    # Check to make sure the fee_config is valid
    fee_config = FeeConfig.objects.filter(fee_config_id=fee_config_id, status='active').first()
    if not fee_config:
        message = {'detail': 'Fee configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if fee_config.product_config != product_config:
        message = {'detail': 'Product config id is not valid'}
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
        
    serializer = FeeConfigSerializer(fee_config, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateFeeConfig(request, product_id, product_config_id, fee_config_id):
    data = request.data
    user = request.user

    # Check to make sure the fee_config is valid
    fee_config = FeeConfig.objects.filter(fee_config_id=fee_config_id, status='active').first()
    if not fee_config:
        message = {'detail': 'Fee configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if fee_config.product_config != product_config:
        message = {'detail': 'Product config id is not valid'}
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
        fee_config.label=data['label']
    if 'day' in data:
        fee_config.day=data['day']
    if 'structure' in data:
        fee_config.structure=data['structure']
    if 'amount' in data:
        fee_config.amount=data['amount']
    
    fee_config.save()
    serializer = FeeConfigSerializer(fee_config, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveFeeConfig(request, product_id, product_config_id, fee_config_id):
    
    user = request.user

    # Check to make sure the fee_config is valid
    fee_config = FeeConfig.objects.filter(fee_config_id=fee_config_id, status='active').first()
    if not fee_config:
        message = {'detail': 'Fee configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if fee_config.product_config != product_config:
        message = {'detail': 'Product config id is not valid'}
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

    fee_config.status = 'archived'
    fee_config.save()
    message = {'detail': 'Fee configuration was archived'}
    return Response(message, status=200)     
