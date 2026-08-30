from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Candidate, Employer, InterviewInvitation


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ["id", "name", "company", "title"]


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "full_name",
            "headline",
            "location",
            "skills",
            "experience_years",
            "education",
            "preferred_role",
            "preferred_salary_min",
            "preferred_work_arrangement",
            "summary",
            "portfolio_url",
        ]


class InterviewInvitationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    employer = EmployerSerializer(read_only=True)
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(), source="candidate", write_only=True
    )
    employer_id = serializers.PrimaryKeyRelatedField(
        queryset=Employer.objects.all(), source="employer", write_only=True
    )
    expires_in_days = serializers.IntegerField(
        write_only=True, required=False, default=7, min_value=1, max_value=30
    )

    class Meta:
        model = InterviewInvitation
        fields = [
            "id",
            "candidate",
            "employer",
            "candidate_id",
            "employer_id",
            "role_title",
            "role_summary",
            "salary_min",
            "salary_max",
            "work_arrangement",
            "reason_for_interest",
            "status",
            "expires_at",
            "expires_in_days",
            "created_at",
            "responded_at",
        ]
        read_only_fields = ["status", "expires_at", "created_at", "responded_at"]

    def validate(self, attrs):
        if attrs.get("salary_max", 0) < attrs.get("salary_min", 0):
            raise serializers.ValidationError(
                {"salary_max": "Maximum salary must be greater than or equal to minimum."}
            )
        return attrs

    def create(self, validated_data):
        expires_in_days = validated_data.pop("expires_in_days", 7)
        validated_data["expires_at"] = timezone.now() + timedelta(days=expires_in_days)
        return super().create(validated_data)


class InvitationResponseSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "save", "decline"])
