from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# email verificatoin
class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)


# Category Model
class Category(models.Model):
    title  = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=250)
    content = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    img = models.ImageField(upload_to='post_img/')

    def __str__(self):
        return self.title


# comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title