# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from json import dumps
import json
import requests

# Create your views here.
def new_request(request):
   
    template = "new_request.html"
    template_vars = {}

    if request.method == 'POST':
        # on python 3
        temp = str(request.body, 'utf-8')
        json_data = json.loads(temp)
        print(json_data)
        
    return render(request, template, template_vars)
