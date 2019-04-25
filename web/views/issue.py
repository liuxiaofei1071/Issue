from web.models import Issue,TeamProjt
from django.shortcuts import render
from web.forms import GitForm
from utils.pagination import Pagination
from django.http import JsonResponse, HttpResponse
from django.template.response import TemplateResponse
from utils.gitfile import Gitclass
import logging

logging.basicConfig(
    level = 10
)

#展示发布列表
def update_list(request):
   search = request.GET.get('table_search','')
   updateall = Issue.objects.filter(team__name__contains=search)
   page = Pagination(request.GET.get('page'),updateall.count(),request.GET.copy(),5)

   return TemplateResponse(request, 'menu/updatelist.html',
                           {'updateall':updateall[page.start:page.end],'page_title':'更新列表','page_html':page.page_html})

#展示回滚列表
def rollback_list(request):
   search = request.GET.get('table_search','')
   updateall = Issue.objects.filter(team__name__contains=search,status="7")
   page = Pagination(request.GET.get('page'),updateall.count(),request.GET.copy(),5)

   return TemplateResponse(request, 'menu/updatelist.html',
                           {'updateall':updateall[page.start:page.end],'page_title':'回滚列表','page_html':page.page_html})

#新增/编辑发布
def create_git(request,pk=None):
   issue = Issue.objects.filter(pk=pk).first()
   form_obj = GitForm(instance=issue)
   title="编辑" if pk else "添加"
   if request.method == 'POST':
      form_obj = GitForm(request.POST,instance=issue)
      if form_obj.is_valid():
         form_obj.save()
         return JsonResponse({'status':0,'msg':f'{title}成功'})
      else:
         return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
   return render(request, 'create/git_create.html', {'form_obj':form_obj, "pk":pk})

#获取发布
def get_bra(request,pk):
    logging.error('这是一个pk',pk)
    team = TeamProjt.objects.filter(pk=pk).first()
    bras = Gitclass(team.name, team.git_path).get_bra()  #btas拿到所有分支
    return JsonResponse({"status": 0, "data": bras})  #返回json数据给前端ajax
"""
#宝哥测试bug
def aa(request):
    logging.error('1111111111')
    return HttpResponse(123)
"""