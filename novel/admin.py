from django.contrib import admin
from .models import Author,Book,Publisher
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display=['salutation','first_name','last_name','email','bio','birth_date','profile_picture']
admin.site.register(Author,AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display=['id','title','author_id','publisher_id','publication_date']
admin.site.register(Book,BookAdmin)

class PublisherAdmin(admin.ModelAdmin):
    list_display=['id','name','address','city','state','country','established_year','contact_number','is_active']
admin.site.register(Publisher,PublisherAdmin)