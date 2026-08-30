from pathlib import Path

from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path
from django.views.decorators.cache import never_cache

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "frontend_dist"


@never_cache
def spa_index(_request):
    index = FRONTEND_DIST / "index.html"
    if not index.exists():
        raise Http404("Frontend build missing. Run npm run build and copy dist/ to frontend_dist/.")
    return FileResponse(index.open("rb"), content_type="text/html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", spa_index, name="spa"),
]
