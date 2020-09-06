from django.contrib import admin
from blog.models import CustomUser,Post,Comment,Like
from blog.forms import UserCreateForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
