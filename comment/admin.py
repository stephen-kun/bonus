from django.contrib import admin
from .models import *

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment,CommentAdmin)
