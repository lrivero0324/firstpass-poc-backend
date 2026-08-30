from django.db import models
from django.utils import timezone


class Employer(models.Model):
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=160)
    title = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company})"


class Candidate(models.Model):
    WORK_REMOTE = "remote"
    WORK_HYBRID = "hybrid"
    WORK_ONSITE = "onsite"
    WORK_CHOICES = [
        (WORK_REMOTE, "Remote"),
        (WORK_HYBRID, "Hybrid"),
        (WORK_ONSITE, "On-site"),
    ]

    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=200)
    location = models.CharField(max_length=120)
    skills = models.JSONField(default=list)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=200)
    preferred_role = models.CharField(max_length=120)
    preferred_salary_min = models.PositiveIntegerField()
    preferred_work_arrangement = models.CharField(max_length=20, choices=WORK_CHOICES)
    summary = models.TextField()
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class InterviewInvitation(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_SAVED = "saved"
    STATUS_DECLINED = "declined"
    STATUS_EXPIRED = "expired"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_SAVED, "Saved for Later"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_EXPIRED, "Expired"),
    ]

    WORK_CHOICES = Candidate.WORK_CHOICES

    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="invitations"
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="invitations"
    )
    role_title = models.CharField(max_length=160)
    role_summary = models.TextField()
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    work_arrangement = models.CharField(max_length=20, choices=WORK_CHOICES)
    reason_for_interest = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def refresh_expiration(self):
        if (
            self.status in {self.STATUS_PENDING, self.STATUS_SAVED}
            and timezone.now() >= self.expires_at
        ):
            self.status = self.STATUS_EXPIRED
            self.save(update_fields=["status"])
        return self

    def __str__(self):
        return f"{self.role_title} → {self.candidate.full_name}"
