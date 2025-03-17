from django.contrib import admin
from django.urls import include, path
from core.views import profile,error
urlpatterns = [
    path('', include("home.urls")),
    # path('', include("home.urls", namespace="home")),
    path('admin/', admin.site.urls),
    path('profile/<str:username>', profile),
    path('error', error),

]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 