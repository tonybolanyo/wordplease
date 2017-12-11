from django.contrib import admin

from .models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated', 'created')
    list_editable = ('name',)


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'updated', 'created', 'pub_date',)

    class Meta:
        model = Post


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
