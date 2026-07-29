from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r"inscriptions", views.InscriptionViewSet)
router.register(r"students", views.StudentViewSet)
router.register(r"teachers", views.TeacherViewSet)
router.register(r"messages", views.MessageViewSet)
router.register(r"activities", views.ActivityLogViewSet)
router.register(r"config", views.SchoolConfigViewSet)

urlpatterns = [
    path("config/public/", views.public_config, name="public_config"),
    path("", include(router.urls)),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("dashboard/stats/", views.dashboard_stats, name="dashboard_stats"),
]
