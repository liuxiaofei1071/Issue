from web.models import Init
from django.shortcuts import render
from web.forms import InitForm
from utils.pagination import Pagination
from django.http import JsonResponse
from django.template.response import TemplateResponse


#展示初始化列表
def init_list(request):
   search = request.GET.get('table_search','')
   inits = Init.objects.filter(name__contains=search)
   page = Pagination(request.GET.get('page'),inits.count(),request.GET.copy(),5)

   return TemplateResponse(request, 'menu/initlist.html',
                           {'inits':inits[page.start:page.end],'page_title':'初始化列表','page_html':page.page_html})

#新增/编辑初始化列表
def change_init(request,pk=None):
   init = Init.objects.filter(pk=pk).first()
   form_obj = InitForm(instance=init)
   title="编辑" if pk else "添加"
   if request.method == 'POST':
      form_obj = InitForm(request.POST,instance=init)
      if form_obj.is_valid():
         form_obj.instance.create_user = request.account
         form_obj.save()
         return JsonResponse({'status':0,'msg':f'{title}成功'})
      else:
         return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
   return render(request, 'create/init_create.html', {'form_obj':form_obj, "pk":pk})


#删除初始化
def del_init(request,pk):
   init = Init.objects.filter(pk=pk).delete()
   if init:
      return JsonResponse({'status':0,'msg':'删除成功'})
   else:
      return JsonResponse({'status': 1, 'msg': '删除失败'})

#初始化详情
def detail_init(request,pk):
   init = Init.objects.filter(pk=pk).first()
   init_all = init.initlog_set.all()  #反向查询初始化日志全部信息
   return render(request,"menu/initlog.html",{"initlogs":init_all})

