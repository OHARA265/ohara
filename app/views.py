from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from datetime import datetime, date, timedelta, time
from django.views.generic import View, TemplateView
from .models import Zaseki, Booking, News
from django.views import generic
from django.utils.timezone import localtime, make_aware
from django.db.models import Q
import qrcode
import base64
from io import BytesIO
from PIL import Image
from accounts.models import CustomUser
# -*- coding: utf-8 -*-
import hashlib
from .forms import BookingForm, NewsUpdateForm, NicknameUpadateForm, BookingViewForm,BookingFreeForm
from .mixin import SuperuserRequiredMixin, StaffRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseBadRequest
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from allauth.account.models  import EmailAddress 
from allauth.account.adapter import DefaultAccountAdapter

# Create your views her
# from io import BytesIOe.

class IndexView(View):

    def get(self, request, *args, **kwargs):
        newsX = News.objects.filter(important__gte = 2).order_by('-important','-day')[:5]
        newsZ = News.objects.filter(important__lte = 1 ).order_by('-day')[:5]
        return render(request,'Index.html',{
        'news1' : newsX,
        'news2' : newsZ,
        })


class QuestionView(TemplateView):
    template_name="question.html"


class ZasekiView(View):

    def get(self, request):
        dayss = datetime.today()
        times = dayss.hour
        min = dayss.minute
        daysss = date.today()
        todays  = daysss + timedelta(days=1)
        x = 1
        xx = 0
        y=0
        booking_data1 = []
        for i in range(15):
            booking_data = Booking.objects.filter(start__gte = dayss, start__lte = todays, zaseki = x).count()
            x += 1
            booking_data1.append(booking_data)
        if times < 10:
            y = 8
        elif times < 11:
            y = 7
        elif times < 12:
            y = 6
        elif times < 13:
            y = 5
        elif times < 14:
            y = 4
        elif times < 15:
            y = 3
        elif times < 16:
            y = 2
        elif times < 17:
            y = 1
        else :
            y = 0

        z = y * 15
        zz = sum(booking_data1)
        yoyaku = []
        for i in booking_data1:
            if i == y:
                zzz = 1               
                yoyaku.append(zzz)
            else:
                yoyaku.append(0)

        zaseki_data = Zaseki.objects.filter(id__lte = '5', id__gt = "0")
        zaseki_data2 = Zaseki.objects.filter(id__lte = '10', id__gt = '5')
        zaseki_data3 = Zaseki.objects.filter(id__lte = '15', id__gt = '10' )

        return render(request, 'booking/zaseki.html',{
            'zaseki_data' : zaseki_data,
            'zaseki_data2' : zaseki_data2,
            'zaseki_data3' : zaseki_data3,
            'booking_data' : booking_data1,
            'y' : y,
            'z' : z,
            'zz' : zz,
            'yoyaku' : yoyaku 
        })


class CalendarView(View):


    def get(self, request, *args, **kwargs):
        zaseki = Zaseki.objects.get(id=self.kwargs['pk'])
        today = date.today()
        todayss = datetime.today()
        day30 = todayss.date() + timedelta(days=30) 
        dayz = todayss.hour
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            # 週始め
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
        # 1週間
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]


        calendar = {}
        # 10時～20時
        for hour in range(10, 18):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
        booking_data = Booking.objects.filter(zaseki=self.kwargs['pk']).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False
            
        return render(request, 'booking/calendar.html', {
            'zaseki_data': zaseki,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
            'dayz' :dayz,
            'dayss' :day30,
        })


class BookingView(View):
    def get(self, request, *args, **kwargs):
        zaseki = Zaseki.objects.get(id=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingForm(request.POST or None)

        return render(request, 'booking/booking.html', {
            'zaseki_data': zaseki,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        zaseki_data = get_object_or_404(Zaseki, id=self.kwargs['pk'])
        booking_dataxxx = get_object_or_404(CustomUser, id=self.request.user.id)
        user = CustomUser.objects.get(pk = self.request.user.id)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        daysss = date.today()
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        days = make_aware(datetime(year=year,month=month,day=day))
        days.weekday()
        booking_data = Booking.objects.filter(zaseki=self.kwargs['pk'], start=start_time)
        booking_data1 = CustomUser.objects.get(pk=self.request.user.id)
        #顧客の予約上限数を判定　予約
        booking_data2 = Booking.objects.filter(customer=self.request.user.id, today=days)
        #顧客が当日の予約上限に達しているか判定　
        booking_data3 = Booking.objects.filter(customer=self.request.user.id, start=start_time)
        #顧客が同じ時間帯で複数予約をしないように設定
        booking_data4 = Booking.objects.filter(customer=self.request.user.id, end=end_time)
        #顧客が同じ時間帯で複数予約をしないように設定

        form = BookingForm(request.POST or None)
        if days.weekday == 0:
            form.add_error(None, '休館日です。\n別の日時で予約をお願いします。')
        elif booking_data.exists():    
            form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
        if days.weekday() == 1:
            form.add_error(None, '休館日です。\n別の日時で予約をお願いします。')
        elif user.is_staff == True:
            booking = Booking()
            booking_data1.booking_kazu
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.data['tel']
            booking.remarks = form.data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
            return redirect('app:thanks') 
        elif booking_data1.booking_kazu  >= 3:
            form.add_error(None, '予約上限に達しています。\n予約上限数は3です。')
        elif booking_data2.exists():
            form.add_error(None, '既に本日分の予約をしております。\n別の日付で予約をお願いします。')
        elif booking_data3.exists():
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif booking_data4.exists(): 
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif form.is_valid():
            booking = Booking()
            booking_data1.booking_kazu += 1
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.cleaned_data['tel']
            booking.remarks = form.cleaned_data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
                                    
            return redirect('app:thanks') 

        return render(request, 'booking/booking.html', {
            'zaseki_data': zaseki_data,
            'user': user,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

#class BookingMulti:


class ThanksView(TemplateView):
    template_name = 'booking/thanks.html'

class BookingDeleteView(View):

    def get(self, request, *args, **kwargs):
        Custom = CustomUser.objects.get(pk = self.request.user.id)
        x = Custom.booking_kazu
        days = date.today()
        booking = Booking.objects.filter(customer = self.request.user.id, today__gte = days).order_by('today')
        return render(request,"bookingdelete.html",{
            "booking_data" : booking
        })
    
    def post(self, request, *args, **kwargs):
        try:
            delete = self.request.POST['delete']
            Booking.objects.filter(pk = delete).delete()
            Custom = CustomUser.objects.get(pk = self.request.user.id)
            if Custom.is_staff == False:
                Custom.booking_kazu -= 1
                Custom.save()
            return redirect('app:mypage') 
        except:
            return redirect('app:error')


class BookingViewView(View):

    def get(self, request, *args, **kwargs):
        todays = date.today()
        booking = Booking.objects.filter(today = todays).order_by("start")
        form = BookingViewForm
        return render(request,'bookingview.html',{
            'booking' : booking,
            'form' : form,
        })
    
    def post(self, request, *args, **kwargs):
        try:
            lastn = self.request.POST["lastname"]
            firstn = self.request.POST["firstname"]
            todays = date.today()
            form = BookingViewForm
            customer1 = CustomUser.objects.filter(last_name__icontains= lastn, first_name__icontains = firstn)
            customer111 = [] 
            for custom in customer1:
                customer11 = Booking.objects.filter(customer = custom.pk,today__gte = todays).order_by("today")
                customer111.extend(customer11)
            error2 = "aaaa"    
            if customer111:
                pass
            else:
                error2 = "検索結果がありません"

            return render(request,'bookingview.html',{
            'customer' : customer111,
            'form' : form,
            'error2' : error2
            })
        except:
            aaa = "検索結果がありません"
            form = BookingViewForm

            return render(request,'bookingview.html',{
                "error" : aaa, 
                'form' : form,
            })


class CalendarFreeView(View):


    def get(self, request, *args, **kwargs):
        today = date.today()
        todayss = datetime.today()
        day30 = todayss.date() + timedelta(days=30) 
        dayz = todayss.hour
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            # 週始め
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
            # 1週間
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        calendarcount = 0
        # 10時～20時
        for hour in range(10, 18):
            row = {}
            for day in days:
                row[day] = 0
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
        booking_data1 = Booking.objects.filter(zaseki=1).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data1:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data2 = Booking.objects.filter(zaseki=2).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data2:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data3 = Booking.objects.filter(zaseki=3).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data3:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data4 = Booking.objects.filter(zaseki=4).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data4:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data5 = Booking.objects.filter(zaseki=5).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data5:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data6 = Booking.objects.filter(zaseki=6).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data6:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data7 = Booking.objects.filter(zaseki=7).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data7:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data8 = Booking.objects.filter(zaseki=8).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data8:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data9 = Booking.objects.filter(zaseki=9).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data9:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data10 = Booking.objects.filter(zaseki=10).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data10:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data11 = Booking.objects.filter(zaseki=11).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data11:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data12 = Booking.objects.filter(zaseki=12).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data12:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data13 = Booking.objects.filter(zaseki=13).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data13:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data14 = Booking.objects.filter(zaseki=14).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data14:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1
        booking_data15 = Booking.objects.filter(zaseki=15).exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data15:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] += 1

        return render(request, 'booking/calendarfree.html', {
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
            'dayz' :dayz,
            'dayss' :day30,
        })


class BookingFreeView(View):
    def get(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingFreeForm(request.POST or None)
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        book = Booking.objects.filter(start = start_time)
        zasekipk = Zaseki.objects.all()
        xx =[]
        xxx = []
        for zasekis in zasekipk:
            xx.append(zasekis.pk)
        for zasekis in book:
            xxx.append(zasekis.zaseki.pk)
        xz = set(xx) - set(xxx)
        xz =list(xz)
        zaseki = Zaseki.objects.get(pk = xz[0])

        return render(request, 'booking/bookingfree.html', {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
            'x' : xz,
            'zaseki' : zaseki,
            'xxx' :xxx,
        })

    def post(self, request, *args, **kwargs):
        zaseki = self.request.POST["zasekiid"]
        zaseki_data = Zaseki.objects.get(pk = zaseki)
        booking_dataxxx = get_object_or_404(CustomUser, id=self.request.user.id)
        user = CustomUser.objects.get(pk = self.request.user.id)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        daysss = date.today()
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
        days = make_aware(datetime(year=year,month=month,day=day))
        booking_data = Booking.objects.filter(zaseki=zaseki_data.pk, start=start_time)
        booking_data1 = CustomUser.objects.get(pk=self.request.user.id)
        #顧客の予約上限数を判定　予約
        booking_data2 = Booking.objects.filter(customer=self.request.user.id, today=days)
        #顧客が当日の予約上限に達しているか判定　
        booking_data3 = Booking.objects.filter(customer=self.request.user.id, start=start_time)
        #顧客が同じ時間帯で複数予約をしないように設定
        booking_data4 = Booking.objects.filter(customer=self.request.user.id, end=end_time)
        #顧客が同じ時間帯で複数予約をしないように設定

        form = BookingFreeForm(request.POST or None)
        if booking_data.exists():    
            form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
        elif start_time.weekday == 1:
            form.add_error(None, '休館日です。\n別の日時で予約をお願いします。')
        elif user.is_staff == True:
            booking = Booking()
            booking_data1.booking_kazu
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.data['tel']
            booking.remarks = form.data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
            return redirect('app:thanks') 
        elif booking_data1.booking_kazu  >= 3:
            form.add_error(None, '予約上限に達しています。\n予約上限数は3です。')
        elif booking_data2.exists():
            form.add_error(None, '既に本日分の予約をしております。\n別の日付で予約をお願いします。')
        elif booking_data3.exists():
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif booking_data4.exists(): 
            form.add_error(None, '既に同じ時間帯で予約があります。\n別の時間で予約をお願いします。')
        elif form.is_valid():
            booking = Booking()
            booking_data1.booking_kazu += 1
            booking.zaseki = zaseki_data
            booking.start = start_time
            booking.end = end_time
            booking.tel = form.cleaned_data['tel']
            booking.remarks = form.cleaned_data['remarks']
            booking.customer = booking_dataxxx
            booking.today = days
            booking.save()
            booking_data1.save()
                                    
            return redirect('app:thanks') 

        return render(request, 'booking/bookingfree.html', {
            'zaseki_data': zaseki_data,
            'user': user,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })



class Search1View(StaffRequiredMixin,TemplateView):
    template_name = 'search/search_a.html'

class Search_bView(StaffRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            yuubin = self.request.GET["yuubin"]
            birth1  = self.request.GET["birth"]
            last = self.request.GET["last_name"]
            first = self.request.GET["first_name"]
            cusyuu = CustomUser.objects.get(post_code = yuubin, birth = birth1, last_name = last, first_name = first)
        except:
            return redirect('app:error') 
        return render(request,"search/search_b.html",{
            "cusyuu" : cusyuu,
                    })

    def post(self, request, *args, **kwargs):
        lastn = self.request.POST["lastn"]
        firstn = self.request.POST["firstn"]
        aaddress = self.request.POST["aaddress"]
        emaila = self.request.POST["emaila"]
        postcode = self.request.POST["postcode"]
        tell1 = self.request.POST["tell1"]
        pk1 = self.request.POST["pk"]
        updateemail = EmailAddress.objects.get(user_id = pk1)
        update1 = CustomUser.objects.get(pk = pk1)
        update1.last_name = lastn
        update1.first_name = firstn
        update1.address = aaddress
        update1.email = emaila
        update1.post_code = postcode
        update1.tel = tell1
        updateemail.email = emaila
        update1.save()
        updateemail.save()
        return redirect('app:done') 

class DoneView(TemplateView):
    template_name = 'search/done.html'

class ErrorView(TemplateView):
    template_name = 'search/error.html'


class MypageView(View):

    def get(self, request, *args, **kwargs):

        user = CustomUser.objects.get(pk =self.request.user.id )
        booking = Booking.objects.filter(customer = self.request.user.id).order_by('-start')[:10]
        return render(request,"mypage.html",{
            "user" : user,
            "booking_data" : booking
                    })



class NewsUpdateView(View,StaffRequiredMixin):

    def get(self, request, *args, **kwargs):
        form = NewsUpdateForm
        today = date.today()

        return render(request,"newsupdate.html",{
            "form" : form,
            "today" : today
                    })

    def post(self, request, *args, **kwargs):
        news = self.request.POST['news']
        title = self.request.POST['title']
        important = self.request.POST['important']
        newsz = News()
        newsz.title = title
        newsz.news = news
        newsz.important = int(important)
        newsz.save()
        return redirect('app:done') 

class NewsUpdate2View(View,StaffRequiredMixin):

    def get(self, request, *args, **kwargs):
        form = NewsUpdateForm
        news = News.objects.get(pk = self.kwargs['pk'])

        return render(request,'newsupdate2.html',{
            "form" : form,
            "newS" : news,
        })

    def post(self, request, *args, **kwargs):
        news = self.request.POST['news']
        title = self.request.POST['title']
        important = self.request.POST['important']
        newsz = News.objects.get(pk = self.kwargs['pk'])
        newsz.title = title
        newsz.news = news
        newsz.important = int(important)
        newsz.save()
        return redirect('app:done') 

class NicknameUpdateView(View):

    def get(self, request, *args, **kwargs):
        form = NicknameUpadateForm
        
        return render(request,"nicknameupdate.html",{
            "form" : form
                    })
    
    def post(self, request, *args, **kwargs):
        nickname = CustomUser.objects.get(pk = self.request.user.id)
        new = self.request.POST['nickname']
        nickname.nickname = new
        nickname.save()
        return redirect('app:done') 


class KisekiView(View):

    def get(self, request, *args, **kwargs):
        raikan_suu = CustomUser.objects.get(pk = self.request.user.id)

        return render(request,'kiseki.html',{
            "kazu" : raikan_suu,
                })


