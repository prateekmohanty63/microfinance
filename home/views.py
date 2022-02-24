# Views
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

# Dates and
from django.utils import timezone
from datetime import datetime, timedelta

# Settings
from django.conf import settings

# Models
from .models import *
from django.db.models import Q

# Forms
from .forms import *

# Celery stuff
from home.tasks import *

# Utils
from home.utils import *


#===============================================================================
# Static Pages
#===============================================================================

def landing(request):
    context = {}
    return render(request, 'home/landing.html', context=context)

def terms(request):
    context = {}
    return render(request, 'home/terms.html', context=context)

def privacy(request):
    context = {}
    return render(request, 'home/privacy.html', context=context)

def about(request):
    context = {}
    return render(request, 'home/about.html', context=context)


#===============================================================================
# Core
#===============================================================================

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home/home.html', context=context)


#===============================================================================
# AWS and S3 stuff
#===============================================================================

# Specific imports for S3
import boto3

@login_required(login_url='login')
@csrf_exempt
def sign_s3(request):
    S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME

    name = request.GET.get('file_name', None)
    file_type = request.GET.get('file_type', None)
    file_extension = pathlib.Path(name).suffix
    file_name = 'private/uploads/' + randomfilestr() + file_extension

    print('File Name:' + file_name)
    print('Type:' + file_type)
    print("File Extension: ", file_extension)

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION
    )

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "private", "Content-Type": file_type},
        Conditions = [
        {"acl": "private"},
        {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    print(presigned_post)
    print('https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name))

    response = JsonResponse({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
    response.status_code = 200
    return response


#===============================================================================
# Bad Urls and Error Handling
#===============================================================================

def error_403(request, exception):
        data = {}
        return render(request,'home/errors/403.html', status=403)

def error_404(request, exception):
        data = {}
        return render(request,'home/errors/404.html', status=404)

def error_500(request):
        return render(request,'home/errors/500.html', status=500)
