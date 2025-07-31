import json
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import Record
from django.core.exceptions import ValidationError
from datetime import datetime

def upload_file(request):
    message = ""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValidationError("Файл должен содержать список объектов.")

                records = []
                for item in data:
                    name = item.get("name")
                    date_str = item.get("date")

                    if not name or not date_str:
                        raise ValidationError("Отсутствует ключ 'name' или 'date'.")

                    if len(name) >= 50:
                        raise ValidationError(f"Строка '{name}' слишком длинная.")

                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
                    except ValueError:
                        raise ValidationError(f"Неверный формат даты: {date_str}")

                    records.append(Record(name=name, date=date))

                # Сохраняем в БД только если ошибок не было
                Record.objects.bulk_create(records)
                message = "Файл успешно загружен и данные сохранены!"
            except (json.JSONDecodeError, ValidationError) as e:
                message = f"Ошибка: {str(e)}"
    else:
        form = UploadFileForm()
    return render(request, "uploader/upload.html", {"form": form, "message": message})


def records_list(request):
    records = Record.objects.all()
    return render(request, "uploader/list.html", {"records": records})
