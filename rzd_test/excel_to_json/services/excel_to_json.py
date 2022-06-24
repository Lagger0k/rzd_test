import pandas
import simplejson
from django.core.files.uploadedfile import InMemoryUploadedFile


def convert_excel_to_jason(file: InMemoryUploadedFile) -> None:
    """Конвертирует файл excel в json. Структура JSON файла должна быть сформирована на основе вкладок в Excel файле.
    Наименования атрибутов объекта верхнего уровня должны совпадать с именами листов в Excel-файле.
    Наименования атрибутов вложенных объектов, должны определяться наименованиями соответствующих столбцов в заголовке
    соответствующих таблиц."""
    json_file_name = file.__str__().split('.')[0] + '.json'
    data = pandas.read_excel(file, sheet_name=None)
    data_dict = dict()

    for name, df in data.items():
        df.update(df.select_dtypes('datetime').apply(lambda x: x.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
        data_dict[name] = df.to_dict(orient='records')

    with open(json_file_name, 'w') as file:
        simplejson.dump(data_dict, file, indent=4, ensure_ascii=False, default=str, ignore_nan=True)
