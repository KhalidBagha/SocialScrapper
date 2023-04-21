from django.shortcuts import render
from .models import *
def dashboard(request):
    fbcount = Facebook_Pages.objects.all().count()
    lnpagecount = Linkedin_Pages.objects.all().count()
    lnempcount = Linkedin_Emp.objects.all().count()

    fb = Facebook_Pages.objects.order_by('-id')[:5]
    ln = Linkedin_Emp.objects.order_by('-id')[:5]


    context = {
        'fbcount' : fbcount,
        'lnpagecount': lnpagecount,
        'lnempcount' : lnempcount,
        'fb':fb,
        'ln':ln
    }


    return render(request,'stats.html',context)