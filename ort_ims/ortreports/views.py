from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpRequest
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import os
import sys
from rich import inspect

from config.settings.base import BASE_DIR

DATAFILES_DIR = os.path.join(BASE_DIR, "DataFiles")
REPORT_DIR = os.path.join(DATAFILES_DIR, "ortreports")
REPORT_TEMPLATE_DIR = os.path.join(REPORT_DIR, "Template")


# Create your views here.
def amz_report(request: HttpRequest):
    return render(request, "ortreports/amz.html")


def burn_report(request: HttpRequest):
    return render(request, "ortreports/burn.html")


def emc_report(request: HttpRequest):
    return render(request, "ortreports/emc.html")


def harmonic_report(request: HttpRequest):
    if request.method == "GET":
        harmonic_path = os.path.join(REPORT_TEMPLATE_DIR, "harmonic")
        har_templates = []
        for template in os.listdir(harmonic_path):
            id = template.split(" ")[0]
            har_templates.append({"id": id, "name": template})
        return render(request, "ortreports/harmonic.html", {"templates": har_templates})
    if request.method == "POST":
        from libs.makereports.harmonic import make_harmonic_report

        har_report = request.FILES
        inspect(har_report.values())
        return render(request, "ortreports/harmonic.html")
