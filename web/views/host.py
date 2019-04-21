from web.models import Host
from django.shortcuts import render
from web.forms import HostForm
from utils.pagination import Pagination
from django.template.response import TemplateResponse
from django.http import JsonResponse


#展示主机列表
def host_list(request):
    search = request.GET.get('table_search','')
    hosts = Host.objects.filter(name__contains=search)
    page = Pagination(request.GET.get('page'),hosts.count(),request.GET.copy(),5)

    return TemplateResponse(request, 'menu/hostlist.html',
                           {'hosts': hosts[page.start:page.end], 'page_title': '主机列表', 'page_html': page.page_html})

#新增/编辑主机
def change_host(request,pk=None):
    host = Host.objects.filter(pk=pk).first()
    form_obj = HostForm(instance=host)
    title="编辑" if pk else "添加"
    if request.method == 'POST':

        form_obj = HostForm(request.POST,instance=host)
        if form_obj.is_valid():

            form_obj.save()
            return JsonResponse({'status':0,'msg':f'{title}成功'})
        else:
            return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
    return render(request, 'create/host_create.html', {'form_obj':form_obj, "pk":pk})

#删除用户
def del_host(request,pk):

    host = Host.objects.filter(pk=pk).delete()
    if host:
        return JsonResponse({'status':0,'msg':'删除成功'})
    else:
        return JsonResponse({'status':1,'msg':'删除失败'})