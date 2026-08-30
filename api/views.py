from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Candidate, Employer, InterviewInvitation
from .serializers import (
    CandidateSerializer,
    EmployerSerializer,
    InterviewInvitationSerializer,
    InvitationResponseSerializer,
)


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    """Search and filter candidate profiles — core employer-first capability."""

    serializer_class = CandidateSerializer

    def get_queryset(self):
        qs = Candidate.objects.all()
        skill = self.request.query_params.get("skill")
        location = self.request.query_params.get("location")
        role = self.request.query_params.get("role")
        work = self.request.query_params.get("work_arrangement")
        min_experience = self.request.query_params.get("min_experience")
        max_salary = self.request.query_params.get("max_salary")

        if location:
            qs = qs.filter(location__icontains=location)
        if role:
            qs = qs.filter(preferred_role__icontains=role)
        if work:
            qs = qs.filter(preferred_work_arrangement=work)
        if min_experience:
            qs = qs.filter(experience_years__gte=int(min_experience))
        if max_salary:
            qs = qs.filter(preferred_salary_min__lte=int(max_salary))

        # JSONField skill match works across SQLite and Postgres for this POC.
        if skill:
            needle = skill.strip().lower()
            matched_ids = [
                candidate.id
                for candidate in qs
                if any(needle in str(item).lower() for item in (candidate.skills or []))
            ]
            qs = qs.filter(id__in=matched_ids)
        return qs


class EmployerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer


class InterviewInvitationViewSet(viewsets.ModelViewSet):
    """Employer-initiated interview invitations with candidate responses."""

    serializer_class = InterviewInvitationSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        qs = InterviewInvitation.objects.select_related("candidate", "employer")
        candidate_id = self.request.query_params.get("candidate")
        employer_id = self.request.query_params.get("employer")
        status_filter = self.request.query_params.get("status")

        if candidate_id:
            qs = qs.filter(candidate_id=candidate_id)
        if employer_id:
            qs = qs.filter(employer_id=employer_id)
        if status_filter:
            qs = qs.filter(status=status_filter)

        for invitation in qs:
            invitation.refresh_expiration()
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object().refresh_expiration()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def respond(self, request, pk=None):
        invitation = self.get_object().refresh_expiration()

        if invitation.status == InterviewInvitation.STATUS_EXPIRED:
            return Response(
                {"detail": "This invitation has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if invitation.status in {
            InterviewInvitation.STATUS_ACCEPTED,
            InterviewInvitation.STATUS_DECLINED,
        }:
            return Response(
                {"detail": f"Invitation already {invitation.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvitationResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action_name = serializer.validated_data["action"]

        mapping = {
            "accept": InterviewInvitation.STATUS_ACCEPTED,
            "save": InterviewInvitation.STATUS_SAVED,
            "decline": InterviewInvitation.STATUS_DECLINED,
        }
        invitation.status = mapping[action_name]
        if action_name != "save":
            invitation.responded_at = timezone.now()
        invitation.save()
        return Response(InterviewInvitationSerializer(invitation).data)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "employer-first-poc"})
