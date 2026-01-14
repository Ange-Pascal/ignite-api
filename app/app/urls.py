"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema', SpectacularAPIView.as_view(), name="api-schema"),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs"
    ),
    path("api/users/", include("users.urls")),
    path("api/instructors/", include("instructors.urls", namespace="instructor")),  # <-- namespace ici
    path("api/", include("categories.urls")),
    path("api/", include("courses.urls")),
    path("api/", include("modules.urls")),
    path("api/", include("lessons.urls")),
    path("api/", include("outcomes.urls")),
    path("api/", include("highlights.urls")),
    path("api/", include("reviews.urls")),
    path("api/", include("carts.urls")),
    path("api/", include("cartitems.urls" ,  namespace="cartitems")),
    path('api/', include('checkouts.urls')),
    path("api/", include("paymentmethods.urls")),
    path("api/", include("payments.urls")),
    path("api/", include("videos.urls")),
    path("api/", include("typequizs.urls")),
    path("api/", include("typequestions.urls")),
    path("api/", include("typeresponses.urls")),
    path("api/", include("quizs.urls")),
    path("api/", include("quizquestions.urls")),
    path("api/", include("quizoptions.urls")),
    path("api/", include("quizattempts.urls")),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
