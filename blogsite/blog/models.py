from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from PIL import Image
# Create your models here.

class CustomUser(AbstractUser):
    blocked = models.ManyToManyField('CustomUser',related_name='blocked_users',blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    post_banner = models.ImageField(upload_to='images/')
    author = models.ForeignKey(CustomUser,related_name='posts',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.post_banner:
            image = Image.open(self.post_banner)
            height, width = image.size
            h,w = height,width
            if height > 450:
                h = 450
            elif width > 800:
                w = 800
            image = image.resize((w,h), Image.ANTIALIAS)
            image.save(self.post_banner.path)
            image.close()


class Comment(models.Model):
    author = models.ForeignKey(CustomUser,related_name='user_comments',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='post_comments',on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_created']


    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})

    def __str__(self):
        return self.text





class Like(models.Model):
    author = models.ForeignKey(CustomUser,related_name='likedby',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='postlikes',on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
