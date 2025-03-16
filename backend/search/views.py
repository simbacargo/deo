import json
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# from decorators import ajax_required
from django.shortcuts import render
from django.views.generic import ListView
from home.models import Product

from django.contrib.auth import get_user_model

def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            # return redirect('/search/')
            pass


        try:
                search_type = request.GET.get('type')
                if search_type not in ['parts','users']:
                    search_type = 'feed'

        except Exception:
                search_type = 'feed'

        count = {}
        results = {}
        results	['products'] = Product.objects.filter(name__icontains=querystring,)
        return render(request,template_name="search.html",context=results)