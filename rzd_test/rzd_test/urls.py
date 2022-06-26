from django.contrib import admin
from django.urls import path
from excel_to_json.views import upload_excel_file, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/excel', upload_excel_file),
    path('', index, name='home')
]
