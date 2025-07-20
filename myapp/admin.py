from django.contrib import admin

# Register your models here.
from .models import Author,Subject, Bookshelf,Book,Format
admin.site.register(Author)
admin.site.register(Subject)
admin.site.register(Bookshelf)
admin.site.register(Book)
admin.site.register(Format)
