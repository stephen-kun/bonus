from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from weixin.models import Consumer
from .models import *

User = get_user_model()

class TopicAdmin(admin.ModelAdmin):
    pass


class SliderImageAdmin(admin.ModelAdmin):
    pass





class ConsumerInline(admin.StackedInline):
    model = Consumer


class ConsumerUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('date_joined', 'last_login', 'is_staff', 'is_superuser', 'is_active',)
    inlines = (ConsumerInline,)

admin.site.unregister(User)
admin.site.register(User, ConsumerUserAdmin)

admin.site.register(Topic,TopicAdmin)
admin.site.register(SliderImage,SliderImageAdmin)



####################################################
# from functools import update_wrapper
# from django.contrib import admin
# from django.contrib.admin import ModelAdmin
# from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import render
#
# from .models import *
# from forms import *
#
#
# class TopicAdmin(ModelAdmin):
#     change_form_template = 'admin/topic/change_form.html'
#     manage_view_template = 'admin/topic/manage_view.html'
#
#     def get_urls(self):
#         from django.conf.urls import patterns, url
#
#         def wrap(view):
#             def wrapper(*args, **kwargs):
#                 return self.admin_site.admin_view(view)(*args, **kwargs)
#             return update_wrapper(wrapper, view)
#
#         info = self.model._meta.app_label, self.model._meta.model_name
#
#         urls = patterns('',
#             url(r'^(.+)/manage/$',
#                 wrap(self.manage_view),
#                 name='%s_%s_manage' % info),
#         )
#
#         super_urls = super(TopicAdmin, self).get_urls()
#
#         return urls + super_urls
#
#     def manage_view(self, request, id, form_url='', extra_context=None):
#         opts = Topic._meta
#         form = TopicForm()
#         obj = Topic.objects.get(pk=id)
#
#         if not self.has_change_permission(request, obj):
#             raise PermissionDenied
#
#         # do cool management stuff here
#
#         preserved_filters = self.get_preserved_filters(request)
#         form_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, form_url)
#
#         context = {
#             'title': 'Manage %s' % obj,
#             'has_change_permission': self.has_change_permission(request, obj),
#             'form_url': form_url,
#             'opts': opts,
#             'errors': form.errors,
#             'app_label': opts.app_label,
#             'original': obj,
#         }
#         context.update(extra_context or {})
#
#         return render(request, self.manage_view_template, context)
# admin.site.register(Topic, TopicAdmin)
