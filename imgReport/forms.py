#coding:utf-8

from django import forms
from imgReport.models import User

class UserLoginInfo(forms.Form):
    userName = forms.CharField(required=True,min_length=3)
    passWord = forms.CharField(required=True,min_length=3)


class UserRegisterForm(forms.Form):
    userName = forms.CharField(required=True,min_length=3)
    email = forms.CharField(required=True,min_length=3)
    passWord1 = forms.CharField(required=True, min_length=3)
    passWord = forms.CharField(required=True,min_length=3)



    def clean_userName(self):
        userName = self.cleaned_data.get('userName',None)
        oldUserName =User.objects.filter(username=userName).first()
        print '-----------',oldUserName
        if oldUserName:
            raise forms.ValidationError('用户名不能重复',code='repeatError')
        return userName

    def clean_passWord(self):
        passWord = self.cleaned_data.get('passWord',None)
        passWord1 = self.cleaned_data.get('passWord1',None)
        if passWord != passWord1:
            raise forms.ValidationError('两次密码输入不正确',code='notEval')
        return passWord

class PermisForm(forms.Form):

    name = forms.CharField(required=True)
    url = forms.CharField(required=True)