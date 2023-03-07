from django.contrib import admin
from authentification.models import User


class columnsTableUser(admin.ModelAdmin):
    list_display=[field.name for field in User._meta.fields]
    
admin.site.register(User, columnsTableUser)
# Register your models here.
