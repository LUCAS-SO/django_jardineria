from django.contrib import admin
from django.utils.html import format_html
from .models import Job, JobPhoto, Location, Tag


class JobPhotoInline(admin.TabularInline):
    model = JobPhoto
    extra = 1
    fields = ('before_after', 'photo', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="120" />', obj.photo.url)
        return "No image"
    preview.allow_tags = True


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'duration', 'created_at')
    list_filter = ('date', 'location')
    search_fields = ('description',)
    inlines = [JobPhotoInline]
    ordering = ('-date', '-created_at')
    autocomplete_fields = ('tags',)

    def short_description(self, obj):
        return (obj.description[:50] + '...') if len(obj.description) > 50 else obj.description

@admin.register(JobPhoto)
class JobPhotoAdmin(admin.ModelAdmin):
    list_display = ('job', 'before_after', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" />', obj.photo.url)
        return "No image"
    thumbnail.allow_tags = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)