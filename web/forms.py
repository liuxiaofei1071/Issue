from django import forms
from web.models import User
from web.models import Host
from web.models import Cron
from django.forms import ModelForm

#定义bootstrap样式
class BootstranpModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstranpModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

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
    # 后端实现分时日月周
    # minute = forms.ChoiceField(label='分钟',choices=[ (i,i) for i in range(60)])
    # hour = forms.ChoiceField(label='小时',choices=[ (i,i) for i in range(24)])
    # day = forms.ChoiceField(label='天',choices=[ (i,i) for i in range(32)])
    # month = forms.ChoiceField(label='月',choices=[ (i,i) for i in range(1,13)])
    # weekday = forms.ChoiceField(label='周',choices=[ (i,i) for i in range(0,7)])

    class Meta:
        model = Cron
        exclude = ["create_user", "time"]


