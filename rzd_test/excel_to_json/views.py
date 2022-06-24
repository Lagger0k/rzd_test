from django.shortcuts import render
from excel_to_json.services.excel_to_json import convert_excel_to_jason


def intro(request):
    return render(request, 'intro.html')


def upload_excel_file(request):
    if request.POST:
        file = request.FILES['file']
        convert_excel_to_jason(file)
        return render(request, 'confirmation.html')
    return render(request, 'excel.html')
