from web.models import Command,Host
from django.shortcuts import render
from web.forms import CommandForm
from utils.pagination import Pagination
from django.template.response import TemplateResponse
from django.http import JsonResponse
from utils.ansible2.runner import CommandRunner
from utils.ansible2.inventory import Inventory


#展示主机列表
def command_list(request):
    search = request.GET.get('table_search','')
    if request.account.is_admin == "0":
        commands = Command.objects.filter(command__contains=search)
    else:
        commands = Command.objects.filter(command__contains=search,user=request.account)
    page = Pagination(request.GET.get('page'),commands.count(),request.GET.copy(),5)

    return TemplateResponse(request, 'menu/commandlist.html',
                           {'commands': commands[page.start:page.end], 'page_title': '命令列表', 'page_html': page.page_html})

#新增/编辑主机
def change_command(request):
    """
        var zNodes =[
    			{ id:1, pId:0, name:"随意勾选 1", open:true},
    			{ id:11, pId:1, name:"随意勾选 1-1"},
    			{ id:12, pId:1, name:"随意勾选  1-2", open:true},
    		];
    		pid 是父id
    		open:true 是否展开
     host_data = [
            {
                "hostname": "10.211.55.19",
                "ip": "10.211.55.19",
                "port": 22,
                "username": "root",
            },
        ]
        inventory = Inventory(host_data)  #动态生成组
        runner = CommandRunner(inventory)

        res = runner.execute('pwd')
        # print(res.results_command)
        print(res.results_raw,type(res.results_raw))
        :param request:
        :param pk:
        :return:
        """
    host_nodes = [{"id": 1, "pId": 0, "name": "主机列表", "open": "true"}]
    for h in Host.objects.all():
        host_nodes.append({"id": 11, "pId": 1, "name": h.ip})

    if request.method == 'POST':
        nodes = request.POST.getlist("nodes[]")
        hosts_list = Host.objects.filter(ip__in=nodes)
        host_data = [{"hostname": h.ip, "ip": h.ip, "port": h.ssh} for h in hosts_list]
        inventory = Inventory(host_data)  # 动态生成组
        runner = CommandRunner(inventory)
        res = runner.execute(request.POST.get("command"))
        print(res.results_raw)
        Command.objects.create(command=request.POST.get("command"),user=request.account,hosts_list=nodes,result=res.results_raw)
        return JsonResponse({"status": 0, "msg": res.results_raw})
    return TemplateResponse(request, 'create/command_create.html', {'nodes':host_nodes, "page_title":"执行命令"})

