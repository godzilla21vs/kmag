from .models import *
from django.contrib import admin

# Register your models here.

class imageInLine(admin.StackedInline):
    model = post_image
    extra = 1

class itemAdmin(admin.ModelAdmin):
    inlines = [imageInLine]

admin.site.register(Category,)
admin.site.register(Utilisateur,)
admin.site.register(Tags,)
admin.site.register(Author,)
admin.site.register(Post,itemAdmin)
admin.site.register(News,)
admin.site.register(Subscriber,)