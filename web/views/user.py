from web.models import User
from django.shortcuts import render
from web.forms import UserForm
from utils.pagination import Pagination
from django.http import JsonResponse
from django.template.response import TemplateResponse


#展示用户列表
def user_list(request):
   search = request.GET.get('table_search','')
   users = User.objects.filter(username__contains=search)
   page = Pagination(request.GET.get('page'),users.count(),request.GET.copy(),5)

   return TemplateResponse(request, 'menu/userlist.html',
                           {'users':users[page.start:page.end],'page_title':'用户列表','page_html':page.page_html})



#新增/编辑用户
def change_user(request,pk=None):
   user = User.objects.filter(pk=pk).first()
   form_obj = UserForm(instance=user)
   title="编辑" if pk else "添加"
   if request.method == 'POST':
      form_obj = UserForm(request.POST,instance=user)
      if form_obj.is_valid():
         form_obj.save()
         return JsonResponse({'status':0,'msg':f'{title}成功'})
      else:
         return JsonResponse({'status':1,'msg':f'{title}失败,失败的原因是{form_obj.errors}'})
   return render(request, 'create/user_create.html', {'form_obj':form_obj, "pk":pk})




#删除用户
def del_user(request,pk):
   user = User.objects.filter(pk=pk).delete()
   print(user)
   return JsonResponse({'status':0,'msg':'删除成功'})