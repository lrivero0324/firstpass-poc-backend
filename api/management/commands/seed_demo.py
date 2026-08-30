from django.core.management.base import BaseCommand

from api.models import Candidate, Employer


class Command(BaseCommand):
    help = "Seed demo employers and candidate profiles for the POC"

    def handle(self, *args, **options):
        Employer.objects.all().delete()
        Candidate.objects.all().delete()

        employers = [
            Employer.objects.create(
                name="Maya Chen",
                company="Northstar Digital",
                title="Talent Partner",
            ),
            Employer.objects.create(
                name="Jordan Blake",
                company="Harbor Health Systems",
                title="Hiring Manager",
            ),
        ]

        candidates = [
            {
                "full_name": "Alex Rivera",
                "headline": "Junior Frontend Developer",
                "location": "Miami, FL",
                "skills": ["React", "JavaScript", "CSS", "Accessibility"],
                "experience_years": 2,
                "education": "B.S. Information Technology - FIU",
                "preferred_role": "Frontend Developer",
                "preferred_salary_min": 70000,
                "preferred_work_arrangement": "hybrid",
                "summary": "Builds clean, accessible interfaces and wants roles where employers reach out with clear role details.",
                "portfolio_url": "https://example.com/alex",
            },
            {
                "full_name": "Sam Okonkwo",
                "headline": "Full-Stack Engineer",
                "location": "Remote",
                "skills": ["Python", "Django", "React", "PostgreSQL"],
                "experience_years": 4,
                "education": "M.S. Computer Science - UF",
                "preferred_role": "Full-Stack Engineer",
                "preferred_salary_min": 95000,
                "preferred_work_arrangement": "remote",
                "summary": "Ships end-to-end product features and prefers transparent salary and work-arrangement details up front.",
                "portfolio_url": "https://example.com/sam",
            },
            {
                "full_name": "Priya Nair",
                "headline": "UX Designer",
                "location": "Orlando, FL",
                "skills": ["Figma", "User Research", "Prototyping", "Design Systems"],
                "experience_years": 3,
                "education": "B.F.A. Graphic Design - UCF",
                "preferred_role": "Product Designer",
                "preferred_salary_min": 80000,
                "preferred_work_arrangement": "hybrid",
                "summary": "Turns research into usable product flows; open to interview invites that explain why the team is interested.",
                "portfolio_url": "https://example.com/priya",
            },
            {
                "full_name": "Chris Delgado",
                "headline": "Data Analyst",
                "location": "Tampa, FL",
                "skills": ["SQL", "Python", "Tableau", "Excel"],
                "experience_years": 5,
                "education": "B.S. Statistics - USF",
                "preferred_role": "Data Analyst",
                "preferred_salary_min": 85000,
                "preferred_work_arrangement": "onsite",
                "summary": "Turns messy datasets into decisions. Looking for teams that value matching over mass applications.",
                "portfolio_url": "https://example.com/chris",
            },
            {
                "full_name": "Taylor Kim",
                "headline": "Marketing Operations Specialist",
                "location": "Atlanta, GA",
                "skills": ["HubSpot", "Campaign Analytics", "Copywriting", "SEO"],
                "experience_years": 3,
                "education": "B.A. Communications - Emory",
                "preferred_role": "Marketing Operations",
                "preferred_salary_min": 65000,
                "preferred_work_arrangement": "remote",
                "summary": "Coordinates campaign ops and reporting; prefers invitations that include salary range and role summary.",
                "portfolio_url": "https://example.com/taylor",
            },
            {
                "full_name": "Jordan Ellis",
                "headline": "Backend Developer",
                "location": "Austin, TX",
                "skills": ["Django", "REST APIs", "Docker", "AWS"],
                "experience_years": 6,
                "education": "B.S. Software Engineering - UT Austin",
                "preferred_role": "Backend Engineer",
                "preferred_salary_min": 110000,
                "preferred_work_arrangement": "hybrid",
                "summary": "Designs reliable APIs and data models. Open to employer-first outreach with a clear reason for interest.",
                "portfolio_url": "https://example.com/jordan",
            },
        ]

        for data in candidates:
            Candidate.objects.create(**data)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(employers)} employers and {len(candidates)} candidates."
            )
        )
