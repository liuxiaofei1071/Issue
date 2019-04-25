from django import forms
from web.models import User
from web.models import Host
from web.models import Cron
from web.models import TeamProjt
from web.models import Command
from web.models import Init
from web.models import InitLog
from web.models import Issue
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

#项目Form
class TeamForm(BootstranpModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #选择相关人员的时候,只显示对应的人员,开发,测试,运维人员
        self.fields['developer'].choices = [(d.pk,d.username) for d in User.objects.filter(role="0")]
        self.fields['tester'].choices = [(t.pk,t.username) for t in User.objects.filter(role="1")]
        self.fields['ops_user'].choices = [(o.pk,o.username) for o in User.objects.filter(role="2")]


    class Meta:
        model = TeamProjt
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.instance.pk:
            name_obj = Host.objects.filter(name=name).exclude(pk=self.instance.pk)
        else:
            name_obj = Host.objects.filter(name=name)

        if name_obj:
            raise forms.ValidationError('项目已存在')
        return name

#命令Form
class CommandForm(BootstranpModelForm):

    class Meta:
        model = Command
        fields = "__all__"

#初始化Form
class InitForm(BootstranpModelForm):

    class Meta:
        model = Init
        fields = "__all__"

    def clean_function(self):
        func = self.cleaned_data['func']
        if self.instance.pk:
            func_obj = User.objects.filter(func=func).exclude(pk=self.instance.pk)
        else:
            func_obj = User.objects.filter(func=func)

        if func_obj:
            raise forms.ValidationError('该功能已初始化')

        return func

# 初始化日志Form
class InitLogForm(BootstranpModelForm):

    class Meta:
        model = InitLog
        fields = ['init','hosts_list']

#发布
#初始化Form
class GitForm(BootstranpModelForm):

    class Meta:
        model = Issue
        fields =["team","backup"]

