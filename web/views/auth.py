import hashlib
from django.shortcuts import render,redirect,reverse
from web import models


#登录
def login(request):
   error_msg = ''
   if request.method == 'POST':
      user = request.POST.get('username')
      pwd = request.POST.get('password')
      print(user,pwd)
      # md5 = hashlib.md5()
      # md5.update(password.encode('utf-8'))
      # password = md5.hexdigest()
      obj = models.User.objects.filter(username=user,password=pwd).first()
      if obj:
         request.session['user_id'] = obj.pk
         return redirect(reverse('user_list'))
      else:
         error_msg = '用户名或密码错误'
   return render(request,'auth/login.html',{'error_msg':error_msg})

#退出
def logout(request):
   request.session.flush()
   return redirect(reverse('login'))