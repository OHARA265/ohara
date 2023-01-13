from django import forms

from accounts.models import CustomUser

from .models import News

from app.mixin import SuperuserRequiredMixin,StaffRequiredMixin



class BookingForm(forms.Form):
    tel = forms.CharField(max_length=30, label='電話番号')
    remarks = forms.CharField(label='備考')

class BookingFreeForm(forms.Form):
    tel = forms.CharField(max_length=30, label='電話番号')
    remarks = forms.CharField(label='備考') 
    zasekiid = forms.CharField(widget=forms.HiddenInput())

class NewsUpdateForm(forms.Form,StaffRequiredMixin):
    title = forms.CharField(max_length=50,label='タイトル')
    important = forms.fields.ChoiceField(
        choices = (
            ('1', 1),
            ('2', 2),
            ('3', 3),),
            label='重要度', widget=forms.widgets.Select, initial=1)
    news = forms.CharField(max_length=1000,label='お知らせ', widget=forms.Textarea())

class BookingViewForm(forms.Form):
    lastname = forms.CharField(max_length=50, required=False)
    firstname = forms.CharField(max_length=50, required=False)

class NicknameUpadateForm(forms.Form):
    nickname =forms.CharField(max_length=20,label="ニックネーム")


#class BookingDeleteForm(fomrs.Form):
