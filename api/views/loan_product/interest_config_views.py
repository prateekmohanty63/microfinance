from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loans.models import Product, ProductConfig, InterestConfig
from api.serializers import LoanInterestConfigSerializer as InterestConfigSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createInterestConfig(request, product_id, product_config_id):
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
        interest_config = InterestConfig.objects.create(
            interest_config_id=randomstr(),
            product_config=product_config,
            day=data['day'],
            structure=data['structure'],
            created_user=user,
        )

        if 'amount' in data:
            interest_config.amount=data['amount']
            interest_config.save()
        if 'label' in data:
            interest_config.label=data['label']
            interest_config.save()

        serializer = InterestConfigSerializer(interest_config, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this interest configuration'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getInterestConfigs(request, product_id, product_config_id):
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
    
    interest_configs = InterestConfig.objects.filter(
        product_config=product_config,
        status='active',
    ).order_by('day')

    page = request.query_params.get('page')
    paginator = Paginator(interest_configs, 5)

    try:
        interest_configs = paginator.page(page)
    except PageNotAnInteger:
        interest_configs = paginator.page(1)
    except EmptyPage:
        interest_configs = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = InterestConfigSerializer(interest_configs, many=True)
    return Response({'interest_configs': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getInterestConfig(request, product_id, product_config_id, interest_config_id):

    user = request.user

    # Check to make sure the interest_config is valid
    interest_config = InterestConfig.objects.filter(interest_config_id=interest_config_id, status='active').first()
    if not interest_config:
        message = {'detail': 'Interest configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if interest_config.product_config != product_config:
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
        
    serializer = InterestConfigSerializer(interest_config, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateInterestConfig(request, product_id, product_config_id, interest_config_id):
    data = request.data
    user = request.user

    # Check to make sure the interest_config is valid
    interest_config = InterestConfig.objects.filter(interest_config_id=interest_config_id, status='active').first()
    if not interest_config:
        message = {'detail': 'Interest configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if interest_config.product_config != product_config:
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
        interest_config.label=data['label']
    if 'day' in data:
        interest_config.day=data['day']
    if 'structure' in data:
        interest_config.structure=data['structure']
    if 'amount' in data:
        interest_config.amount=data['amount']
    
    interest_config.save()
    serializer = InterestConfigSerializer(interest_config, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveInterestConfig(request, product_id, product_config_id, interest_config_id):
    
    user = request.user

    # Check to make sure the interest_config is valid
    interest_config = InterestConfig.objects.filter(interest_config_id=interest_config_id, status='active').first()
    if not interest_config:
        message = {'detail': 'Interest configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Check to make sure the product_config is valid
    product_config = ProductConfig.objects.filter(product_config_id=product_config_id, status='active').first()
    if not product_config:
        message = {'detail': 'Product configuration does not exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if interest_config.product_config != product_config:
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

    interest_config.status = 'archived'
    interest_config.save()
    message = {'detail': 'Interest configuration was archived'}
    return Response(message, status=200)     
