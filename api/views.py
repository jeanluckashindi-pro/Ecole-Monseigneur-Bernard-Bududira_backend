from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Inscription, Student, Teacher, Message, ActivityLog, SchoolConfig
from .serializers import (
    InscriptionSerializer, InscriptionListSerializer,
    StudentSerializer, TeacherSerializer,
    MessageSerializer, MessageCreateSerializer,
    ActivityLogSerializer, SchoolConfigSerializer,
)


class InscriptionViewSet(viewsets.ModelViewSet):
    queryset = Inscription.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return InscriptionListSerializer
        return InscriptionSerializer

    def perform_create(self, serializer):
        inscription = serializer.save()
        ActivityLog.objects.create(
            action="inscription",
            description=f"{inscription.student_first_name} {inscription.student_last_name} "
                        f"a soumis une demande d'inscription."
        )

    @action(detail=True, methods=["patch"])
    def accept(self, request, pk=None):
        inscription = self.get_object()
        inscription.status = "Acceptee"
        inscription.save()
        ActivityLog.objects.create(
            action="inscription_accepted",
            description=f"Inscription de {inscription.student_first_name} "
                        f"{inscription.student_last_name} acceptee."
        )
        return Response({"status": "acceptee"})

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):
        inscription = self.get_object()
        inscription.status = "Rejetee"
        inscription.save()
        ActivityLog.objects.create(
            action="inscription_rejected",
            description=f"Inscription de {inscription.student_first_name} "
                        f"{inscription.student_last_name} rejetee."
        )
        return Response({"status": "rejetee"})


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        teacher = serializer.save()
        ActivityLog.objects.create(
            action="teacher_added",
            description=f"Nouvel enseignant {teacher.first_name} {teacher.last_name} ajoute au systeme."
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        message = serializer.save()
        ActivityLog.objects.create(
            action="message",
            description=f"Nouveau message de {message.name} recu."
        )

    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({"status": "lu"})


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()[:20]
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]


class SchoolConfigViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolConfig.objects.all()
    serializer_class = SchoolConfigSerializer
    permission_classes = [AllowAny]
    lookup_field = "key"


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_inscriptions = Inscription.objects.count()
    pending_inscriptions = Inscription.objects.filter(status="En attente").count()
    accepted_inscriptions = Inscription.objects.filter(status="Acceptee").count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    unread_messages = Message.objects.filter(is_read=False).count()
    total_messages = Message.objects.count()

    level_distribution = (
        Student.objects.values("current_class")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    recent_inscriptions = InscriptionListSerializer(
        Inscription.objects.all()[:6], many=True
    ).data
    recent_activities = ActivityLogSerializer(
        ActivityLog.objects.all()[:6], many=True
    ).data

    return Response({
        "inscriptions": {
            "total": total_inscriptions,
            "pending": pending_inscriptions,
            "accepted": accepted_inscriptions,
        },
        "students": {"total": total_students},
        "teachers": {"total": total_teachers},
        "messages": {
            "total": total_messages,
            "unread": unread_messages,
        },
        "level_distribution": level_distribution,
        "recent_inscriptions": recent_inscriptions,
        "recent_activities": recent_activities,
    })


@api_view(["GET", "PUT"])
@permission_classes([AllowAny])
def public_config(request):
    if request.method == "GET":
        configs = SchoolConfig.objects.all()
        data = {c.key: c.value for c in configs}
        return Response(data)
    config_data = request.data
    for key, value in config_data.items():
        SchoolConfig.objects.update_or_create(key=key, defaults={"value": value})
    return Response({"status": "ok"})
