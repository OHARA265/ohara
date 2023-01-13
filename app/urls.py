from django.urls import path

from . import views

app_name='app'

urlpatterns = [
    path('',views.IndexView.as_view(),name="index"),
    path('question',views.QuestionView.as_view(),name='question'),
    path('mypage',views.MypageView.as_view(),name='mypage'),
    path('kiseki/',views.KisekiView.as_view(),name='kiseki'),
    path('bookingdelete/',views.BookingDeleteView.as_view(),name='bookingdelete'),
    path('search/',views.Search1View.as_view(),name='search_a'),
    path('newsupdate/',views.NewsUpdateView.as_view(),name='newsupdate'),
    path('newsupdate2/<int:pk>/',views.NewsUpdate2View.as_view(),name='newsupdate2'),
    path('nicknameupdate/',views.NicknameUpdateView.as_view(),name="nicknameupdate"),
    path('search_kekka/',views.Search_bView.as_view(),name='search_b'),
    path('done',views.DoneView.as_view(),name="done"),
    path('error',views.ErrorView.as_view(),name="error"),
    path('zaseki/',views.ZasekiView.as_view(),name='zaseki'),
    path('calendar/<int:pk>/', views.CalendarView.as_view(), name='calendar'), # 追加
    path('calendar/<int:pk>/<int:year>/<int:month>/<int:day>/', views.CalendarView.as_view(), name='calendar'), # 追加
    path('calendar/', views.CalendarFreeView.as_view(), name='calendarfree'), # 追加
    path('calendar/<int:year>/<int:month>/<int:day>/', views.CalendarFreeView.as_view(), name='calendarfree'), # 追加
    path('booking/<int:pk>/<int:year>/<int:month>/<int:day>/<int:hour>/', views.BookingView.as_view(), name='booking'), # 追加
    path('booking/<int:year>/<int:month>/<int:day>/<int:hour>/', views.BookingFreeView.as_view(), name='bookingfree'), # 追加
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('bookingview/',views.BookingViewView.as_view(),name='bookingview'),
    ]