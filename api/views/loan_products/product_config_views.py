from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loans.models import Product, ProductConfig
from api.serializers import LoanProductConfigSerializer as ProductConfigSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductConfig(request, product_id):
    user = request.user
    data = request.data

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
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
        product_config = ProductConfig.objects.create(
            product_config_id=randomstr(),
            product=product,
            label=data['label'],
            length=data['length'],
            overdue_on_day=data['overdue_on_day'],
            default_on_day=data['default_on_day'],
            created_user=user,
        )

        serializer = ProductConfigSerializer(product_config, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this product configuration'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProductConfigs(request, product_id):
    user = request.user
    data = request.data

    # Check if the product is valid
    product = Product.objects.filter(product_id=product_id, status='active').first()
    if not product:
        message = {'detail': 'Product does not exist'}
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
    
    product_configs = ProductConfig.objects.filter(
        product=product,
        status='active',
    ).order_by('-created_at')

    page = request.query_params.get('page')
    paginator = Paginator(product_configs, 5)

    try:
        product_configs = paginator.page(page)
    except PageNotAnInteger:
        product_configs = paginator.page(1)
    except EmptyPage:
        product_configs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductConfigSerializer(product_configs, many=True)
    return Response({'product_configs': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProductConfig(request, product_id, product_config_id):

    user = request.user

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
        
    serializer = ProductConfigSerializer(product_config, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProductConfig(request, product_id, product_config_id):
    data = request.data
    user = request.user

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
        product_config.label=data['label']
    if 'length' in data:
        product_config.length=data['length']
    if 'overdue_on_day' in data:
        product_config.overdue_on_day=data['overdue_on_day']
    if 'default_on_day' in data:
        product_config.default_on_day=data['default_on_day']

    product_config.save()
    serializer = ProductConfigSerializer(product_config, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveProductConfig(request, product_id, product_config_id):
    
    user = request.user

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

    product_config.status = 'archived'
    product_config.save()
    message = {'detail': 'Product configuration was archived'}
    return Response(message, status=200)     

  