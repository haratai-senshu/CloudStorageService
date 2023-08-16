from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('product/<pk>/', views.Detail.as_view(), name="detail"),
    path('create/', views.Create.as_view(), name="create"),
    path('delete/<pk>', views.Delete.as_view(), name="delete"),
    path('search', views.SearchView.as_view(), name="search"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
