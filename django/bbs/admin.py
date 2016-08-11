from django.contrib import admin

# Register your models here.
from .models import Client, User, Section, Forum, Post, Reply

class ClientAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
admin.site.register(Client, ClientAdmin)


class UserAdmin(admin.ModelAdmin):
    fields = ['client', 'name', 'email']
admin.site.register(User, UserAdmin)


class SectionAdmin(admin.ModelAdmin):
    fields = ['name', 'admins']
admin.site.register(Section, SectionAdmin)


class ForumAdmin(admin.ModelAdmin):
    fields = ['section', 'name', 'admins']
admin.site.register(Forum, ForumAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'date', 'update', 'topic', 'text', 'forum', 'top', 'newdate']
admin.site.register(Post, PostAdmin)


class ReplyAdmin(admin.ModelAdmin):
    fields = ['author', 'date', 'update', 'text', 'post', 'forum']
admin.site.register(Reply, ReplyAdmin)
