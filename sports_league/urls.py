# sports_league/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('leagues/', include(('leagues.urls', 'leagues'), namespace='leagues')),
    path('matches/', include(('matches.urls', 'matches'), namespace='matches')),
    path('tournaments/', include(('tournaments.urls', 'tournaments'), namespace='tournaments')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
