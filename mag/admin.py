from django.contrib import admin
from .models import *

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