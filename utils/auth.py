from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import reverse,redirect
from web import models

#自定义中间件校验
class AuthenticationMiddlewareMixin(MiddlewareMixin):

    def process_request(self,request):
        if request.path_info.startswith('/admin/'):
            return
        if request.path_info in [reverse('login')]:
            return
        pk = request.session.get('user_id')
        user = models.User.objects.filter(pk=pk).first()
        if user:
            request.account = user
        else:
            return redirect(reverse('login'))

class Response(MiddlewareMixin):
    def process_template_response(self,request,response):
        response.context_data['user'] = request.account
        return response


