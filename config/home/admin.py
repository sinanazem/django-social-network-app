from django.contrib import admin
from .models import PostModel

@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


