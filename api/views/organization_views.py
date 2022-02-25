from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from organizations.models import Organization, OrganizationUser
from api.serializers import OrganizationSerializer, OrganizationSettingsSerializer

from rest_framework import status

from .permissions_check import *
from core.utils import randomstr


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrganization(request):
    user = request.user
    data = request.data

    try:

        # Create the organization
        organization = Organization.objects.create(
            name=data['name'],
            organization_id = randomstr(),
            created_user=user,
        )

        # Create the organization user / created user as an admin
        organization_user = OrganizationUser.objects.create(
            organization=organization,
            user=user,
            role='admin'
        )

        # Create the organization settings with default values
        organization_settings = OrganizationSettings.objects.create(
            organization=organization,
            # Other fields with default values will auto-populate
        )

        serializer = OrganizationSerializer(organization, many=False)
        return Response(serializer.data)
    
    except Exception as e:
        print(e)
        message = {'detail': 'There was an error creating this organization'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrganizations(request):

    user = request.user
    
    # Get the organizations the user is added to
    organization_relations = OrganizationUser.objects.filter(
        user=user,
        status='active',
    )

    # Create array of valid organization ids for the user
    organization_ids = []
    for organization_relation in organization_relations:
        organization_ids.append(organization_relation.organization.id)

    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    organizations = Organization.objects.filter(
        id__in=organization_ids,
        name__icontains=query,
        status='active',
    ).order_by('name')

    page = request.query_params.get('page')
    paginator = Paginator(organizations, 5)

    try:
        organizations = paginator.page(page)
    except PageNotAnInteger:
        organizations = paginator.page(1)
    except EmptyPage:
        organizations = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = OrganizationSerializer(organizations, many=True)
    return Response({'organizations': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrganization(request, organization_id):

    user = request.user
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['user', 'admin'])
    if user_organization['organization']:
        serializer = OrganizationSerializer(user_organization['organization'], many=False)
        return Response(serializer.data)
    else:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
       

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrganization(request, organization_id):
    data = request.data
    user = request.user
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if user_organization['organization']:
        organization = user_organization['organization']
        organization.name = data['name']
        organization.save()
        serializer = OrganizationSerializer(organization, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def archiveOrganization(request, organization_id):
    user = request.user
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if user_organization['organization']:
        organization = user_organization['organization']
        organization.status = 'archived'
        organization.save()
        message = {'detail': 'Organization was archived'}
        return Response(message, status=200)
    else:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrganizationSettings(request, organization_id):

    user = request.user
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if user_organization['organization']:
        organization = user_organization['organization']
        organization_settings = OrganizationSettings.objects.filter(organization=organization).first()
        serializer = OrganizationSettingsSerializer(organization_settings, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
       

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrganizationSettings(request, organization_id):
    data = request.data
    user = request.user
    user_organization = check_organization_permissions(user=user, organization_id=organization_id, roles=['admin'])
    if user_organization['organization']:
        organization = user_organization['organization']
        organization_settings = OrganizationSettings.objects.filter(organization=organization).first()
        organization_settings.multiple_loans_per_customer = data['multiple_loans_per_customer']
        organization_settings.save()
        serializer = OrganizationSettingsSerializer(organization_settings, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': user_organization['message']}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)