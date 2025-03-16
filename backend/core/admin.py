from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Video)


class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'caption','file' ]


admin.site.register(Photo,ProductAdmin)
