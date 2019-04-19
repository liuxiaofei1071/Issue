from django.urls import reverse

def reverse_url(request,name,*args,**kwargs):
    next = request.GET.get('next')
    if next:
        return next
    else:
        return reverse(name,args=args,kwargs=kwargs)
