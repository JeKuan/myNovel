from django.db import models
from django.contrib.auth.models import User #導入內建使用者的模組
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from read_stat.models import ReadNumExpandMethod, ReadDetail
# Create your models here.

class BlogType(models.Model):  #部落格文章類型
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add = True)
    last_updated_time = models.DateTimeField(auto_now = True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)

    def __str__(self):
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    

    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
    '''

    class Meta:
        ordering = ['-created_time']

'''
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)
'''