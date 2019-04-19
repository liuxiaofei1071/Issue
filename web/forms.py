from django import forms
from web.models import User
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