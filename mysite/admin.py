from django.contrib.admin import site
from  .models import Post, Meter, Comment, Profile

site.register(Post)
site.register(Meter)
site.register(Comment)
site.register(Profile)