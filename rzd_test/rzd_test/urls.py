from django.contrib import admin
from django.urls import path
from excel_to_json.views import upload_excel_file, intro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/excel', upload_excel_file),
    path('', intro, name='home')
]
