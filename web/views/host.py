from web.models import Host
from django.shortcuts import render
from web.forms import HostForm
from utils.pagination import Pagination
from django.template.response import TemplateResponse
from django.http import JsonResponse
from utils.ansible2.runner import AdHocRunner
from utils.ansible2.inventory import Inventory


# 展示主机列表
def host_list(request):
    search = request.GET.get('table_search', '')
    hosts = Host.objects.filter(name__contains=search)
    page = Pagination(request.GET.get('page'), hosts.count(), request.GET.copy(), 5)

    return TemplateResponse(request, 'menu/hostlist.html',
                            {'hosts': hosts[page.start:page.end], 'page_title': '主机列表', 'page_html': page.page_html})


# 新增/编辑主机
def change_host(request, pk=None):
    host = Host.objects.filter(pk=pk).first()
    form_obj = HostForm(instance=host)
    title = "编辑" if pk else "添加"
    if request.method == 'POST':
        form_obj = HostForm(request.POST, instance=host)
        if form_obj.is_valid():
            # 校验form后 使用ansible检验机器是否在线
            host_data = [
                {
                    "hostname": form_obj.cleaned_data["ip"],  # 获取主机ip
                    "ip": form_obj.cleaned_data["ip"],
                    "port": form_obj.cleaned_data["ssh"],
                },
            ]  # 主机列表
            inventory = Inventory(host_data)  # 动态生成主机配置信息
            runner = AdHocRunner(inventory)
            tasks = [
                {"action": {"module": "ping"}}
            ]
            ret = runner.run(tasks)
            print(ret.results_summary)
            print(ret.results_raw)
            """
{
	'contacted': ['192.168.220.134'],
	'dark': {}
}
{
	'ok': {
		'192.168.220.134': {
			'ping': {
				'invocation': {
					'module_args': {
						'data': 'pong'
					}
				},
				'ping': 'pong',
				'_ansible_parsed': True,
				'_ansible_no_log': False,
				'changed': False
			}
		}
	},
	'failed': {},
	'unreachable': {},
	'skipped': {}
}
            """
            if not ret.results_raw["ok"]:
                return JsonResponse({'status': 1, 'msg': f'添加失败,失败的原因是主机不可达,请检查网络或ssh_key'})
            form_obj.save()
            return JsonResponse({'status': 0, 'msg': f'{title}成功'})
        else:
            return JsonResponse({'status': 1, 'msg': f'{title}失败,失败的原因是{form_obj.errors}'})
    return render(request, 'create/host_create.html', {'form_obj': form_obj, "pk": pk})


# 删除用户
def del_host(request, pk):
    host = Host.objects.filter(pk=pk).delete()
    if host:
        return JsonResponse({'status': 0, 'msg': '删除成功'})
    else:
        return JsonResponse({'status': 1, 'msg': '删除失败'})
