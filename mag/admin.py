from .models import *
from django.contrib import admin

# Register your models here.

class imageInLine(admin.StackedInline):
    model = post_image
    extra = 1

class itemAdmin(admin.ModelAdmin):
    inlines = [imageInLine]

class MainImageInline(admin.StackedInline):
    model = MainImage

class ThumbnailInline(admin.StackedInline):
    model = Thumbnail

class PostAdmin(admin.ModelAdmin):
    inlines = [MainImageInline, ThumbnailInline]

class MainImageNewsInline(admin.StackedInline):
    model = MainImageNews

class ThumbnailNewsInline(admin.StackedInline):
    model = ThumbnailNews

class NewsAdmin(admin.ModelAdmin):
    inlines = [MainImageNewsInline, ThumbnailNewsInline]

admin.site.register(News, NewsAdmin)

admin.site.register(Post, PostAdmin)
admin.site.register(Category,)
admin.site.register(Utilisateur,)
admin.site.register(Tags,)
admin.site.register(Author,)
admin.site.register(Subscriber,)