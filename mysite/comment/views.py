from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse
from django.http import JsonResponse
from .forms import CommentForm
from django.core.mail import send_mail
from django.utils.timezone import localtime
from django.conf import settings

def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    
    data = {}
    
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
      
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()

        comment.send_mail()
       
        
        #返回數據
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        data ['comment_time'] =  localtime(comment.comment_time).strftime("%Y-%m-%d %H:%M:%S")
       
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)


    '''
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user

    #數據檢查
    if not user.is_authenticated:
        return render(request, 'error.html', {'message':'用戶尚未登錄', 'redirect_to':referer})
    text = request.POST.get('text','').strip()
    if text == '':
        return render(request, 'error.html', {'message':'評論內容不得為空', 'redirect_to':referer}) 


    try:
        content_type = request.POST.get('content_type','')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message':'評論對象不存在', 'redirect_to':referer}) 
    
    #檢查通過，保存數據
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    
    return redirect(referer)
    '''

