from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CandidateViewSet, EmployerViewSet, InterviewInvitationViewSet, health

router = DefaultRouter()
router.register("candidates", CandidateViewSet, basename="candidate")
router.register("employers", EmployerViewSet, basename="employer")
router.register("invitations", InterviewInvitationViewSet, basename="invitation")

urlpatterns = [
    path("health/", health, name="health"),
    path("", include(router.urls)),
]
