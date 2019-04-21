from web.models import Command
from django.shortcuts import render
from web.forms import CommandForm
from utils.pagination import Pagination
from django.template.response import TemplateResponse
from django.http import JsonResponse


#展示主机列表
def command_list(request):
    search = request.GET.get('table_search','')
    commands = Command.objects.filter(command__contains=search)
    page = Pagination(request.GET.get('page'),commands.count(),request.GET.copy(),5)

    return TemplateResponse(request, 'menu/commandlist.html',
                           {'commands': commands[page.start:page.end], 'page_title': '命令列表', 'page_html': page.page_html})

#新增/编辑主机
def change_command(request,pk=None):
    command = Command.objects.filter(command=pk).first()
    form_obj = CommandForm(instance=command)
    title="编辑" if pk else "添加"
    if request.method == 'POST':

        form_obj = CommandForm(request.POST,instance=command)
        if form_obj.is_valid():
            form_obj.instance.create_user = request.account
            form_obj.save()
            return JsonResponse({'status':0,'msg':f'{title}成功'})
        else:
            return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
    return TemplateResponse(request, 'create/command_create.html', {'form_obj':form_obj, "pk":pk,"page_title":"新增命令"})

#删除用户
def del_command(request,pk):
    command = Command.objects.filter(pk=pk).delete()
    if command:
        return JsonResponse({'status':0,'msg':'删除成功'})
    else:
        return JsonResponse({'status':1,'msg':'删除失败'})