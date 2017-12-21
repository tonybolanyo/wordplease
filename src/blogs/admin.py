from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated', 'created')
    list_editable = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'updated', 'created', 'pub_date',)


admin.site.site_title = 'WordPlease Admin'
admin.site.site_header = admin.site.site_title
