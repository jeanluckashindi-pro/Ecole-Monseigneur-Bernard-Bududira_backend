from rest_framework import serializers
from .models import Inscription, Student, Teacher, Message, ActivityLog, SchoolConfig, Media


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class InscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ["id", "student_first_name", "student_last_name", "school_level",
                  "requested_class", "status", "created_at"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["created_at"]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["name", "email", "phone", "subject", "body"]


class MediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["id", "image", "url", "alt_text", "created_at"]
        read_only_fields = ["created_at"]

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"
        read_only_fields = ["created_at"]


class SchoolConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolConfig
        fields = ["key", "value"]
