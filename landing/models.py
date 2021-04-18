from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import PIL
from PIL import Image
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, Adjust, ResizeToFill

class Faq(models.Model):
    title = models.CharField(max_length=500, default='Новый ответ')
    text = models.TextField(blank=True)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

def news_pic_path(instance, filename):
    return 'news/%s/picture/%s' % (instance.date.strftime("%Y-%m-%d"), filename)

class News(models.Model):
    title = models.CharField(max_length=500, default='Новая новость')
    picture = models.ImageField(upload_to=news_pic_path, default='news/default/default_pic.jpg')
    picture_small = ImageSpecField(processors=[ResizeToFill(250, 75)], source='picture', format='JPEG', options={'quality': 60})
    text = models.TextField(blank=True)

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class RoadMap(models.Model):
    title = models.CharField(max_length=500, default='Новая цель')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
