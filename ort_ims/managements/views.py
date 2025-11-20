from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from django.views import generic

# Create your views here.

from ort_ims.common.views import *

from ort_ims.managements.models import (
    TTechnician,
    TProductType,
    TCustCode,
    TTestItem,
)
from ort_ims.managements.forms import *


################# Technicians #################


def technicians(request):
    all_technicians = TTechnician.objects.all()
    context = {
        "all_technicians": all_technicians,
        "title": "测试人员管理",
    }
    return render(request, "managements/technicians.html", context)


def edit_technicians(request, technician_id=0):
    return render_edit_form(
        request,
        TTechnician,
        TechnicianForm,
        technician_id,
        "managements/edit_table1.html",
        "technicians",
        "测试人员编辑",
    )


def add_technicians(request):
    return render_add_form(
        request,
        TechnicianForm,
        "managements/edit_table1.html",
        "technicians",
        "测试人员添加",
    )


def delete_technicians(request, technician_id):
    return handle_delete(request, TTechnician, technician_id, "technicians")


################# TestItems #################


def testitems(request):
    all_testitems = TTestItem.objects.all()
    context = {
        "all_testitems": all_testitems,
        "title": "测试项目管理",
    }
    return render(request, "managements/testitems.html", context)


def edit_testitems(request, testitem_id=0):
    return render_edit_form(
        request,
        TTestItem,
        TestItemForm,
        testitem_id,
        "managements/edit_table1.html",
        "testitems",
        "测试项目编辑",
    )


def add_testitems(request):
    return render_add_form(
        request,
        TestItemForm,
        "managements/edit_table1.html",
        "testitems",
        "测试项目添加",
    )


def delete_testitems(request, testitem_id):
    return handle_delete(request, TTestItem, testitem_id, "testitems")


################# CustProducts #################


def custproducts(request):
    all_customers = TCustCode.objects.all()
    all_products = TProductType.objects.all()
    context = {
        "all_customers": all_customers,
        "all_products": all_products,
        "title": "客户与产品管理",
    }
    return render(request, "managements/custproducts.html", context)


def edit_customers(request, customer_id=0):
    return render_edit_form(
        request,
        TCustCode,
        CustCodeForm,
        customer_id,
        "managements/edit_table1.html",
        "custproducts",
        "客户编辑",
    )


def add_customers(request):
    return render_add_form(
        request,
        CustCodeForm,
        "managements/edit_table1.html",
        "custproducts",
        "客户添加",
    )


def delete_customers(request, customer_id):
    return handle_delete(request, TCustCode, customer_id, "custproducts")


def edit_products(request, product_id=0):
    return render_edit_form(
        request,
        TProductType,
        ProductTypeForm,
        product_id,
        "managements/edit_table1.html",
        "custproducts",
        "产品编辑",
    )


def add_products(request):
    return render_add_form(
        request,
        ProductTypeForm,
        "managements/edit_table1.html",
        "custproducts",
        "产品添加",
    )


def delete_products(request, product_id):
    return handle_delete(request, TProductType, product_id, "custproducts")
