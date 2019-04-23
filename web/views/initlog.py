from web.forms import InitLogForm
from django.shortcuts import render
from django.http import JsonResponse
from utils.ansible2.runner import PlayBookRunner
from utils.ansible2.inventory import Inventory


def create_initlog(request):
    form = InitLogForm()
    if request.method == "POST":
        form = InitLogForm(request.POST)
        if form.is_valid():
            form.instance.user=request.account
            host_data=[{"hostname":h.ip,"ip":h.ip,'port':h.ssh} for h in form.cleaned_data["hosts_list"]]
            inventory = Inventory(host_data)
            runner = PlayBookRunner(inventory).run(form.cleaned_data["init"].playbook)
            form.save()
            return JsonResponse({"status": 0, "msg": "添加成功"})
        else:
            return JsonResponse({"status": 1, "msg": "添加失败,失败的原因是{}".format(form.errors)})
    return render(request, "create/initlog_create.html", {"form": form})

# #新增初始化日志
# def createlog(request):
#    form_obj = InitLogForm()
#    if request.method == 'POST':
#       form_obj = InitLogForm(request.POST)
#       if form_obj.is_valid():
#          form_obj.instance.user = request.account
#          host_data = [{'hostname':h.ip,"ip":h.ip,"port":h.ssh} for h in form_obj.cleaned_data["hosts_list"]]
#          inventory = Inventory(host_data)
#          runner = PlayBookRunner(inventory).run(form_obj.cleaned_data['init'].playbook)
#          form_obj.save()
#          return JsonResponse({'status':0,'msg':'添加成功'})
#       else:
#          return JsonResponse({'status':1,'msg':'添加失败,失败的原因是{form_obj.errors}'})
#    return render(request, 'create/initlog_create.html', {'form_obj':form_obj})
#
