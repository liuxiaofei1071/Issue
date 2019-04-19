from django.shortcuts import render
import time
from django.http import JsonResponse


def home(request):
    return render(request,"master/home.html",{"page_title":"回滚列表"})

def index(request):
    time.sleep(10)
    return JsonResponse({"status":0,"msg":"ok"})