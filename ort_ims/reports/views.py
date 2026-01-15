from pathlib import Path

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from rich import inspect

from config.settings.base import BASE_DIR

DATAFILES_DIR = Path(BASE_DIR) / "DataFiles"
REPORT_DIR = (DATAFILES_DIR) / "reports"
REPORT_TEMPLATE_DIR = (REPORT_DIR) / "Template"


# Create your views here.
def amz_report(request: HttpRequest):
    return render(request, "reports/amz.html")


def burn_report(request: HttpRequest):
    return render(request, "reports/burn.html")


def emc_report(request: HttpRequest):
    return render(request, "reports/emc.html")


def harmonic_report(request: HttpRequest):
    if request.method == "GET":
        harmonic_path = REPORT_TEMPLATE_DIR / "harmonic"
        har_templates = []
        for template in Path.iterdir(harmonic_path):
            harmonic_id = template.split(" ")[0]
            har_templates.append({"id": harmonic_id, "name": template})
        return render(request, "reports/harmonic.html", {"templates": har_templates})
    if request.method == "POST":

        har_report = request.FILES
        inspect(har_report.values())
        return render(request, "reports/harmonic.html")
    return None
