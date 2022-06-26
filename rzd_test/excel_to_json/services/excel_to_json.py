import os
import pandas
import simplejson

from django.core.files.uploadedfile import InMemoryUploadedFile
from celery import shared_task
from rzd_test import settings


@shared_task
def convert_excel_to_json(file_path: str) -> bool:
    """Конвертирует файл excel в json. Структура JSON файла должна быть сформирована на основе вкладок в Excel файле.
    Наименования атрибутов объекта верхнего уровня должны совпадать с именами листов в Excel-файле.
    Наименования атрибутов вложенных объектов, должны определяться наименованиями соответствующих столбцов в заголовке
    соответствующих таблиц."""
    try:
        json_file_name = _create_json_name(file_path)
        data = pandas.read_excel(file_path, sheet_name=None)
        data_dict = dict()
        for name, df in data.items():
            df.update(df.select_dtypes('datetime').apply(lambda x: x.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
            data_dict[name] = df.to_dict(orient='records')

        with open(json_file_name, 'w') as file:
            simplejson.dump(data_dict, file, indent=4, ensure_ascii=False, default=str, ignore_nan=True)
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        os.remove(file_path)


def save_file(file_name: str, file: InMemoryUploadedFile) -> str | None:
    """Сохраняет файл из POST в папку, и возвращает путь к нему, чтобы потом его можно было передать в celery.
    Передать напрямую нельзя, так как тип InMemoryUploadedFile не сериализуемый тип данных"""
    try:
        with open(os.path.join(settings.BASE_DIR, file_name), 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        file_path = os.path.join(settings.BASE_DIR, file_name)
        return file_path
    except Exception as err:
        print(err)
        return None


def check_file_already_exists(file_name: str) -> bool:
    """Проверяет есть ли уже файл json с таким названием."""
    file_path = os.path.join(settings.BASE_DIR, file_name)
    json_file_name = _create_json_name(file_path)
    return os.path.isfile(json_file_name)


def _create_json_name(file_path: str) -> str:
    """Создает название для будущего файла json"""
    json_file_name = file_path.split('.')[0] + '.json'
    return json_file_name
