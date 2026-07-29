from django.contrib import admin
from .models import Inscription, Student, Teacher, Message, ActivityLog, SchoolConfig, Media


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ["student_first_name", "student_last_name", "school_level",
                    "requested_class", "status", "created_at"]
    list_filter = ["status", "school_level"]
    search_fields = ["student_first_name", "student_last_name", "guardian_name"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "school_level", "current_class", "phone"]
    list_filter = ["school_level"]
    search_fields = ["first_name", "last_name", "guardian_name"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "subject", "status"]
    list_filter = ["status"]
    search_fields = ["first_name", "last_name", "subject"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_at"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["action", "description", "created_at"]
    list_filter = ["action"]
    readonly_fields = ["action", "description", "created_at"]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["image", "alt_text", "created_at"]
    search_fields = ["alt_text"]


@admin.register(SchoolConfig)
class SchoolConfigAdmin(admin.ModelAdmin):
    list_display = ["key", "updated_at"]
    search_fields = ["key"]
