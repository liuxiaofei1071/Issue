from web.forms import CronForm
from utils.pagination import Pagination
from web.models import Cron
from django.template.response import TemplateResponse
from django.http import JsonResponse
from utils.ansible2.runner import AdHocRunner
from utils.ansible2.inventory import Inventory


# 展示主机列表
def cron_list(request):
    search = request.GET.get('table_search', '')
    crons = Cron.objects.filter(name__contains=search)
    page = Pagination(request.GET.get('page'), crons.count(), request.GET.copy(), 5)

    return TemplateResponse(request, 'menu/cronlist.html',
                            {'crons': crons[page.start:page.end], 'page_title': '计划任务列表',
                             'page_html': page.page_html})


# 新增/编辑主机
def change_cron(request, pk=0):
    cron = Cron.objects.filter(pk=pk).first()   
    time = None if not pk else cron.time
    form_obj = CronForm(instance=cron)
    title = "编辑" if pk else "添加"
    if request.method == 'POST':
        time = request.POST.getlist("time")
        form_obj = CronForm(request.POST, instance=cron)
        if form_obj.is_valid():
            host_data = []
            form_obj.instance.create_user = request.account
            form_obj.instance.time = time
            for h in form_obj.cleaned_data["host_list"]:
                host_data.append({"hostname": h.ip, "ip": h.ip, "port": h.ssh})  # 主机列表
            print(host_data)
            inventory = Inventory(host_data)  # 动态生成主机配置信息
            runner = AdHocRunner(inventory)
            tasks = [
                {"action": {"module": "cron",
                            "args": f"minute={time[0]} hour={time[1]} day={time[2]} month={time[3]} weekday={time[4]}\
                             name={form_obj.cleaned_data['name']} job={form_obj.cleaned_data['job']} user={form_obj.cleaned_data['user']}"}}
            ]
            ret = runner.run(tasks)
            if not ret.results_raw["ok"]:
                return JsonResponse({'status': 1, 'msg': '添加失败'})
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': f'{title}成功'})
        else:
            return JsonResponse({'status': 1, 'msg': f'{title}失败,失败的原因是{form_obj.errors}'})

    return TemplateResponse(request, 'create/cron_create.html',
                            {'form_obj': form_obj, "pk": pk, "page_title": f"{title}计划任务","time":time})


# 删除用户
def del_cron(request, pk):
    cron = Cron.objects.filter(pk=pk).first()
    host_data = []

    for h in cron.host_list.all():
        host_data.append({"hostname": h.ip, "ip": h.ip, "port": h.ssh})  # 主机列表
    print(host_data)
    inventory = Inventory(host_data)  # 动态生成主机配置信息
    runner = AdHocRunner(inventory)
    tasks = [
        {"action": {"module": 'cron',
                    "args": "name={} user={} state=absent".format(cron.name, cron.user)
                    }}
    ]
    ret = runner.run(tasks)
    if not ret.results_raw["ok"]:
        return JsonResponse({'status': 1, 'msg': '删除失败'})
    cron.delete()
    if cron:
        return JsonResponse({'status': 0, 'msg': '删除成功'})
    else:
        return JsonResponse({'status': 1, 'msg': '删除失败'})
