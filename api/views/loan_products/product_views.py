from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from loans.models import Product
from api.serializers import LoanProductSerializer as ProductSerializer

from rest_framework import status

from api.views.permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProduct(request):
    user = request.user
    data = request.data

    # Check for required params
    if 'organization_id' in data:
        organization_id = data['organization_id']
    else:
        message = {'detail': 'Missing required params'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be creating products (only admins of organizations)
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    organization = user_organization['organization']
    try:

        # Create the product
        product = Product.objects.create(
            name=data['name'],
            product_id=randomstr(),
            organization=organization,
            created_user=user,
        )

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this product'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    user = request.user
    data = request.data

    # Check for required params
    if 'organization_id' in data:
        organization_id = data['organization_id']
    else:
        message = {'detail': 'Missing required params'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # Verify the user has permission to be querying all products from an org (only admins)
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if not user_organization['organization']:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    organization = user_organization['organization']
    
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Product.objects.filter(
        organization=organization,
        name__icontains=query,
        status='active',
    ).order_by('name')

    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProduct(request, product_id):

    user = request.user

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
        
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)    
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProduct(request, product_id):
    data = request.data
    user = request.user

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
        
    product.name = data['name']
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveProduct(request, product_id):
    
    user = request.user

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

    product.status = 'archived'
    product.save()
    message = {'detail': 'Product was archived'}
    return Response(message, status=200)     

  