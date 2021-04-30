"""Data Analyser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from data_analyser_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', views.upload, name="upload"),
    path('api/matrix/<str:file_name>',
         views.get_matrix, name="matrix"),
    path('api/matrix/correlation/<str:file_name>',
         views.calculate_correlation, name="correlation"),
    path('api/matrix/regression/<str:file_name>',
         views.calculate_regression, name="regression"),
    path('api/matrix/series/<str:file_name>',
         views.matrix_to_series, name="series"),
    path('api/columns/<str:file_name>', views.get_columns, name="columns"),
    path('api/columns/side_effect/<str:file_name>',
         views.get_side_effect_columns, name="side_effect"),
    path('api/columns/cells/<str:file_name>',
         views.get_cells_columns, name="cells"),
    path('api/columns/group/<str:file_name>',
         views.group_matrix_by_columns, name="group"),
    path('api/columns/merge/<str:file_name>',
         views.merge_columns, name="merge"),
    path('api/columns/filter/<str:file_name>',
         views.filter_matrix_by_column, name="filter"),
    path('api/test/', views.test),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
