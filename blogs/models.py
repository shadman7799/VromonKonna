from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    thoughts = models.TextField(max_length=1024)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True,
                              default='default_blog.jpg', upload_to='blogs/')

    def __str__(self) -> str:
        return str(self.title) + " -> " + str(self.destination)


class BlogLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.author.email) + " liked " + str(self.blog.title)


class BlogComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    comment = models.TextField(max_length=512)

    def __str__(self) -> str:
        return str(self.author.email) + " commented " + str(self.blog.title)


class PreviewImage(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None)
    image = models.ImageField(null=True, blank=True, upload_to='blogs/')
