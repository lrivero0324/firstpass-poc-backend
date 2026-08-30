from django.contrib import admin

from .models import Candidate, Employer, InterviewInvitation


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "title")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "preferred_role",
        "location",
        "preferred_work_arrangement",
        "experience_years",
    )
    search_fields = ("full_name", "preferred_role", "location", "skills")


@admin.register(InterviewInvitation)
class InterviewInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "role_title",
        "candidate",
        "employer",
        "status",
        "expires_at",
        "created_at",
    )
    list_filter = ("status", "work_arrangement")
