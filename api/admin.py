from django.contrib import admin
from .models import Task
# Register your models here.



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','completed','created_at','updated_at','author')
    list_display_links= ('id','title','created_at')
    list_filter = ("completed",'created_at','updated_at')
    search_fields = ('id','title','description')
    ordering = ("-created_at","-updated_at")
    date_hierarchy = 'created_at'

    def author(self,obj):
        return obj.author.username