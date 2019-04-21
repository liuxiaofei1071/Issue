from django import forms
from web.models import User
from web.models import Host
from web.models import Cron
from django.forms import ModelForm

#定义bootstrap样式
class BootstranpModelForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(BootstranpModelForm,self).__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':"form-control"})

#用户Form
class UserForm(BootstranpModelForm):

    class Meta:
        model = User
        fields = "__all__"

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:
            emobj = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        else:
            emobj = User.objects.filter(email=email)

        if emobj:
            raise forms.ValidationError('邮箱已存在')

        return email

#主机Form
class HostForm(BootstranpModelForm):

    class Meta:
        model = Host
        fields = "__all__"

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        if self.instance.pk:
            ip_obj = Host.objects.filter(ip=ip).exclude(pk=self.instance.pk)
        else:
            ip_obj = Host.objects.filter(ip=ip)

        if ip_obj:
            raise forms.ValidationError('ip已存在')
        return ip

#计划任务Form
class CronForm(BootstranpModelForm):

    class Meta:
        model = Cron
        fields = "__all__"


