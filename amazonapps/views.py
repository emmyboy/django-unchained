# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from parsemyhtml import getAppInfo

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'amazonapps/index.html')

def appinfo(request):
    """
    Input validation function needed here for form entry
    """
    appInfo = getAppInfo(request.POST['amazonappurl'])
    
    return render(request, 'amazonapps/appinfo.html', appInfo)
