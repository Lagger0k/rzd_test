from django.shortcuts import render
from excel_to_json.exceptions import MissingFileError
from excel_to_json.services.excel_to_json import convert_excel_to_json, save_file, check_file_already_exists


def index(request):
    return render(request, 'index.html')


def upload_excel_file(request):
    if request.POST:
        try:
            if not request.FILES:
                raise MissingFileError
            file = request.FILES['file']
            file_name = file.__str__()
            if not check_file_already_exists(file_name):
                saved_file_path = save_file(file_name=file_name, file=file)
                if saved_file_path:
                    convert_excel_to_json.delay(saved_file_path)
                    return render(request, 'confirmation.html')
            else:
                return render(request, 'file_already_exists.html')
        except MissingFileError:
            return render(request, 'miss_excel.html')
    return render(request, 'upload_excel.html')
