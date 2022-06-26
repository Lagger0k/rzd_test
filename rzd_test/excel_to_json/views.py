from django.shortcuts import render
from excel_to_json.services.excel_to_json import convert_excel_to_json, save_file, check_file_already_exists


def intro(request):
    return render(request, 'intro.html')


def upload_excel_file(request):
    if request.POST:
        file = request.FILES['file']
        file_name = file.__str__()
        if not check_file_already_exists(file_name):
            file_path = save_file(file_name=file_name, file=file)
            if file_path:
                convert_excel_to_json.delay(file_path)
                return render(request, 'confirmation.html')
        else:
            return render(request, 'file_already_exists.html')
    return render(request, 'excel.html')
