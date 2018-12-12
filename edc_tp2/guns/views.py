from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404


def home(request):
    


    tparams = {
        
    }
    return render(request, 'index.html', tparams)

