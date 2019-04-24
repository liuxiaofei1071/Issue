from web.models import TeamProjt
from django.shortcuts import render
from web.forms import TeamForm
from utils.pagination import Pagination
from django.template.response import TemplateResponse
from django.http import JsonResponse
from utils.gitfile import Gitclass


#展示项目列表
def team_list(request):
    search = request.GET.get('table_search','')
    teams = TeamProjt.objects.filter(name__contains=search)
    page = Pagination(request.GET.get('page'),teams.count(),request.GET.copy(),5)

    return TemplateResponse(request, 'menu/teamlist.html',
                           {'teams': teams[page.start:page.end], 'page_title': '项目列表', 'page_html': page.page_html})

#新增/编辑项目
def change_team(request,pk=None):
    team = TeamProjt.objects.filter(pk=pk).first()
    form_obj = TeamForm(instance=team)
    title="编辑" if pk else "添加"
    if request.method == 'POST':

        form_obj = TeamForm(request.POST,instance=team)
        if form_obj.is_valid():
            Gitclass(form_obj.cleaned_data['name'],form_obj.cleaned_data['git_path'])
            form_obj.save()
            return JsonResponse({'status':0,'msg':f'{title}成功'})
        else:
            return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
    return render(request, 'create/team_create.html', {'form_obj':form_obj, "pk":pk})

#删除用户
def del_team(request,pk):

    team = TeamProjt.objects.filter(pk=pk).delete()
    if team:
        return JsonResponse({'status':0,'msg':'删除成功'})
    else:
        return JsonResponse({'status':1,'msg':'删除失败'})

#项目详情
def detail_team(request,pk):
    team = TeamProjt.objects.filter(pk=pk).first()
    return render(request,"menu/team_detail.html",{'team':team})