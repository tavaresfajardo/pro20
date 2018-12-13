from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,Http404


def home(request):
    


    tparams = {
        
    }
    return render(request, 'index.html', tparams)


def weapontype(request):
    rg = request.GET
    print('rg',rg)
    type = rg['type']
    print('type',type)
    tparams = {
        
    }
    return render(request, 'weapontype.html', tparams)