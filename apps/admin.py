from django.contrib import admin

from apps.models import Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon', 'type')
    list_display_links = ('id',)
    search_fields = ('name',)
    list_editable = ('name', 'icon', 'type')
    list_per_page = 20
