from organizations.models import *

def check_organization_permissions(user, organization_id, roles):

    response = {}
    organization = Organization.objects.filter(organization_id=organization_id, status='active').first()
    if organization:
        # Confirm the user has access
        organization_user = OrganizationUser.objects.filter(
            organization=organization, 
            user=user, 
            status='active',
            role__in=roles,
        ).first()
        
        if organization_user:
            response['organization'] = organization
            return response
        else: 
            response['organization'] = None
            response['message'] = 'Permission denied'
            return response
    else: 
        response['organization'] = None
        response['message'] = "Organization not found"
        return response