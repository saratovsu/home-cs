from django.contrib.admin import site, register, ModelAdmin, TabularInline
from  .models import Post, Meter, Comment, Profile


@register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'room')


@register(Meter)
class MeterAdmin(ModelAdmin):
    list_display = ('datetime', 'author', 'electric', 'cool', 'hot')
    list_filter = ('datetime', 'author')


class CommentInstanceInline(TabularInline):
    model = Comment

@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('datetime', 'author', 'text')
    inlines = [CommentInstanceInline]


# @register(Comment)
# class ProfileAdmin(ModelAdmin):
#     list_display = ('datetime', 'author', 'post', 'text')



