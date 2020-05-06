import datetime
from django.contrib.contenttypes.models import ContentType

from read_stat.models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum

def read_stat_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = f'{ct.model}_{obj.pk}_read'
    if not request.COOKIES.get(key):
            #總閱讀數+1
            readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
                          
            readnum.read_num += 1
            readnum.save()

            #當天閱讀數+1
            date = timezone.now().date()

            readDetail, _ = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
           
            readDetail.read_num += 1
            readDetail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7] #limit

def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]

def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects \
                .filter(content_type=content_type, date__lt=today, date__gte=date) \
                .values('content_type', 'object_id') \
                .annotate(read_num_sum= Sum('read_num')) \
                .order_by('-read_num') 

    
    return read_details[:7] #limit
