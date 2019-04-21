from web.forms import CronForm
from django.shortcuts import render
from utils.pagination import Pagination
from web.models import Cron
from django.template.response import TemplateResponse
from django.http import JsonResponse




# 展示主机列表
def cron_list(request):
    search = request.GET.get('table_search', '')
    crons = Cron.objects.filter(name__contains=search)
    page = Pagination(request.GET.get('page'), crons.count(), request.GET.copy(), 5)

    return TemplateResponse(request, 'menu/cronlist.html',
                            {'crons': crons[page.start:page.end], 'page_title': '计划任务列表',
                             'page_html': page.page_html})

# 新增/编辑主机
def change_cron(request, pk=None):
    cron = Cron.objects.filter(pk=pk).first()
    form_obj = CronForm(instance=cron)
    title = "编辑" if pk else "添加"
    if request.method == 'POST':

        form_obj = CronForm(request.POST, instance=cron)
        if form_obj.is_valid():
            form_obj.instance.create_user = request.account
            form_obj.instance.time = request.POST.getlist("time")
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': f'{title}成功'})
        else:
            return JsonResponse({'status': 1, 'msg': f'{title}失败,失败的原因是{form_obj.errors}'})
    return TemplateResponse(request, 'create/cron_create.html', {'form_obj': form_obj, "pk": pk,"page_title":"新增计划任务"})

# 删除用户
def del_cron(request, pk):

    cron = Cron.objects.filter(pk=pk).delete()
    if cron:
        return JsonResponse({'status': 0, 'msg': '删除成功'})
    else:
        return JsonResponse({'status': 1, 'msg': '删除失败'})
