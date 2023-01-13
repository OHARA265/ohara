from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import CustomUser,  Booking

def periodic_execution():
    upd_books = []
    todays = date.today()
    booking_data = Booking.objects.filter(today=todays)
    for kazu in booking_data:
        books = kazu.customer.pk
        customuser = CustomUser.objects.get(pk=books)
        customuser.booking_kazu -= 1
        upd_books.append(customuser)



    CustomUser.objects.bulk_update(upd_books, fields=['booking_kazu'])


        
        


def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(periodic_execution, 'cron', hour=18, minute=30)# 毎日実行
  scheduler.start()
