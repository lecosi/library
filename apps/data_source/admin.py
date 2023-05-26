from django.contrib import admin

from apps.data_source.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display_links = None
    list_per_page = 50
    actions = None
    list_filter = ('created_at', )
    list_display = (
        'id',
        'created_at',
        'title',
        'external_id',
        'subtitle',
        'editor',
        'description',
        'publication_date',
    )
