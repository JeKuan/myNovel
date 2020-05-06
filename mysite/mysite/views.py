import datetime
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, redirect
from read_stat.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

def get_n_days_hot_blogs(days=7):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=days)
    blogs = Blog.objects \
    .filter(read_details__date__lt=today, read_details__date__gte=date) \
    .values('id','title') \
    .annotate(read_num_sum = Sum('read_details__read_num')) \
    .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
        
    #獲取7天熱門文章的緩存數據
    seven_hot_data = cache.get('seven_hot_data')
    if seven_hot_data is None:
        seven_hot_data = get_n_days_hot_blogs(days=7)
        cache.set('seven_hot_data', seven_hot_data, 3600)
    else:
        print('Use cache')

    thirty_hot_data = cache.get('thirty_hot_data')
    if thirty_hot_data is None:
        thirty_hot_data = get_n_days_hot_blogs(days=30)
        cache.set('thirty_hot_data', thirty_hot_data, 3600)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_hot_data'] = seven_hot_data
    context['thirty_hot_data'] = thirty_hot_data
    return render(request, 'home.html', context)

