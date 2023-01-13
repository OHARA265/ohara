# forms.py
from allauth.account.forms import SignupForm
from django import forms
from app.mixin import SuperuserRequiredMixin
from .models import CustomUser
from allauth.account.adapter import DefaultAccountAdapter

class CustomSignupForm(SignupForm,SuperuserRequiredMixin): #SignupFormを継承する
    last_name = forms.CharField(label='名字')
    first_name = forms.CharField(label='名前')
    address = forms.CharField(label='住所')
    birth = forms.CharField(label='生年月日')
    tel = forms.IntegerField(label="電話番号",required=False)
    post_code = forms.IntegerField(label="郵便番号")
    
    class Meta:
        model = CustomUser
        
    def signup(self, request,user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.birth = self.cleaned_data['birth']
        user.tel = self.cleaned_data['tel']
        user.post_code = self.cleaned_data['post_code']
        user.save()
        return user


