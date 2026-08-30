"""
WSGI config for config project.

Bootstraps migrations + demo seed on Vercel (/tmp SQLite) so the POC works
without a separate database provision step.
"""

import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()


def _bootstrap_demo_database():
    if not os.environ.get("VERCEL"):
        return
    try:
        from api.models import Candidate

        call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
        if not Candidate.objects.exists():
            call_command("seed_demo", verbosity=0)
    except Exception:
        # Avoid crashing the function cold-start; health/UI can still load.
        pass


_bootstrap_demo_database()
