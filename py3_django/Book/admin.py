from django.contrib import admin
from Book.models import BookInfo, PeopleInfo
# Register your models here.


class PeopleInfoAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'gender', 'book']

class BookInfoAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']



admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(PeopleInfo, PeopleInfoAdmin)