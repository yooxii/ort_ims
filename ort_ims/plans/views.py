from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from django.views import generic

# Create your views here.
from ort_ims.plans.models import (
    TProductType,
    TCustCode,
    TSchedule,
    TCheckouts,
    TTestItem,
    TTechnician,
)
from plans.ortplanforms import *


def index(request):
    return render(request, "ortplans/index.html")


################# Common Functions #################


def render_edit_form(
    request,
    model_class,
    form_class,
    object_id,
    template_name,
    redirect_view_name,
    title_text,
):
    """编辑函数模板

    Args:
        request (request): 网络请求
        model_class (model_class): 模型类
        form_class (form_class): 表单类
        object_id (int): 要编辑的对象ID
        template_name (str): 渲染的html模板名
        redirect_view_name (str): 重定向的视图名
        title_text (str): 网页标题

    Returns:
        (HttpResponse|redirect): 渲染的html或重定向
    """
    if request.method == "GET":
        obj = get_object_or_404(model_class, id=object_id)
        form = form_class(instance=obj)
        return render(request, template_name, {"title": title_text, "form": form})

    obj = get_object_or_404(model_class, id=object_id)
    form = form_class(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(redirect_view_name)
    else:
        return render(request, template_name, {"title": title_text, "form": form})


def render_add_form(request, form_class, template_name, redirect_view_name, title_text):
    """添加函数模板

    Args:
        request (request): 网络请求
        form_class (form_class): 表单类
        template_name (str): 渲染的html模板名
        redirect_view_name (str): 重定向的视图名
        title_text (str): 网页标题

    Returns:
        (HttpResponse|redirect): 渲染的html或重定向
    """

    if request.method == "GET":
        form = form_class()
        return render(request, template_name, {"title": title_text, "form": form})

    form = form_class(request.POST)
    if form.is_valid():
        form.save()
        return redirect(redirect_view_name)
    else:
        return render(request, template_name, {"title": title_text, "form": form})


def handle_delete(request, model_class, object_id, redirect_view_name):
    obj = get_object_or_404(model_class, id=object_id)
    obj.delete()
    return redirect(redirect_view_name)


################# Checkouts #################


class CheckoutsView(generic.ListView):
    model = TCheckouts
    template_name = "ortplans/checkouts.html"


def checkouts(request):
    all_checkouts = TCheckouts.objects.all()
    context = {
        "all_checkouts": all_checkouts,
    }
    return render(request, "ortplans/checkouts.html", context)


def import_checkouts(request):
    return render(request, "ortplans/import_checkouts.html")


def export_checkouts(request):
    return render(request, "ortplans/export_checkouts.html")


def edit_checkouts(request, pk=0):
    model_class = TCheckouts
    form_class = CheckoutForm
    template_name = "ortplans/edit_table1.html"
    object_id = pk
    redirect_view_name = "checkouts"
    title_text = "领用编辑"

    if request.method == "GET":
        obj = get_object_or_404(model_class, id=object_id)
        form = form_class(instance=obj)
        return render(request, template_name, {"title": title_text, "form": form})

    # 返回上一页
    if "back" in request.POST:
        return redirect(redirect_view_name)

    # 初始化表单
    obj: TCheckouts = get_object_or_404(model_class, id=object_id)
    form = form_class(request.POST, request.FILES, instance=obj)

    # 处理删除文件
    clear_file = request.POST.get("sn_file-clear", "off")
    if clear_file == "on":
        obj.sn_file.delete(save=False)

    if form.is_valid():
        old = get_object_or_404(model_class, id=object_id)
        # 如果有新文件上传，先删除旧文件，再保存
        if "sn_file" in request.FILES and old and old.sn_file:
            old.sn_file.delete(save=False)
        form.save()

        # 跳转到排程编辑页面
        if "save_and_schedule" in request.POST:
            sch = TSchedule.objects.filter(Work_Order=obj.Work_Order).first()
            if sch:
                return redirect("edit_schedules", sch.id)
            return redirect("add_schedules", pk=obj.id)
        else:
            return redirect(redirect_view_name)
    else:
        return render(request, template_name, {"title": title_text, "form": form})


def add_checkouts(request):
    template_name = "ortplans/edit_table1.html"
    form_class = CheckoutForm
    redirect_view_name = "checkouts"
    title_text = "领用添加"

    if request.method == "GET":
        form = form_class()
        return render(request, template_name, {"title": title_text, "form": form})

    if "back" in request.POST:
        return redirect(redirect_view_name)
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save()
        if "save_and_schedule" in request.POST:
            return redirect("add_schedules", pk=obj.id)
        else:
            return redirect(redirect_view_name)
    else:
        return render(request, template_name, {"title": title_text, "form": form})


def delete_checkouts(request, pk):
    return handle_delete(request, TCheckouts, pk, "checkouts")


################# Schedules #################


class SchedulesView(generic.ListView):
    model = TSchedule
    template_name = "ortplans/schedules.html"


def import_schedules(request):
    return render(request, "ortplans/import_schedules.html")


def export_schedules(request):
    return render(request, "ortplans/export_schedules.html")


class EditSchedulesView(generic.DetailView):
    model = TSchedule
    form_class = ScheduleForm
    template_name = "ortplans/edit_table1.html"
    redirect_view_name = "schedules"
    title_text = "排程编辑"
    obj = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.obj = self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title_text
        context["form"] = self.form_class(instance=self.obj)
        return context

    def post(self, request, *args, **kwargs):
        if "back" in request.POST:
            return redirect(self.redirect_view_name)
        data = request.POST.copy()
        form = self.form_class(data, instance=self.obj)

        form = deal_schedule_datas(form)
        if form.is_valid():
            form.save()
            return redirect(self.redirect_view_name)
        else:
            return render(
                request, self.template_name, {"title": self.title_text, "form": form}
            )


def deal_schedule_datas(form: ScheduleForm):
    """处理排程表单数据

    Args:
        form (ScheduleForm): 排程表单类实例

    Raises:
        ValidationError: 未找到产品类型
        ValidationError: 未找到客户代码
        ValidationError: 未找到测试项目
        ValidationError: 未提供开始日期
        ValidationError: 未提供机种名或测试项目

    Returns:
        ScheduleForm: 处理后的排程表单实例
    """
    try:
        model = form.data.get("PartNo")
        testing_id = form.data.get("TestItem")
        start_date = form.data.get("StartDate")

        if not model or not testing_id:
            raise ValidationError("PartNo或TestItem未提供")

        obj_product = TProductType.objects.filter(product_code=model[:2]).first()
        obj_customer = TCustCode.objects.filter(cust_code=model[7:9]).first()
        obj_test_item = TTestItem.objects.filter(id=testing_id).first()

        if not obj_product:
            raise ValidationError("根据PartNo未找到对应的产品类型")

        if not obj_customer:
            raise ValidationError("根据PartNo未找到对应的客户代码")

        if not obj_test_item:
            raise ValidationError("根据TestItem未找到对应的测试项目")

        if start_date:
            end_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(
                hours=float(obj_test_item.test_time)
            )
        else:
            raise ValidationError("StartDate未提供")

        form.data.update(
            {
                "Product": obj_product.id,
                "Customer": obj_customer.id,
                "TestPeriod": obj_test_item.test_time,
                "Owner": obj_test_item.test_owner,
                "EndDate": datetime.strftime(end_date, "%Y-%m-%d"),
            }
        )

    except (ValueError, ValidationError) as e:
        form.add_error(None, str(e))

    return form


def add_schedules(request, checkout_id):
    template_name = "ortplans/edit_table1.html"
    redirect_view_name = "schedules"
    title_text = "排程编辑"

    if request.method == "GET":
        ###### 自动生成JobNo ######
        latest_entry = TSchedule.objects.order_by("-id").first()
        latest_job_no = latest_entry.JobNo if latest_entry else "01"
        now = datetime.now()
        year_month = now.strftime("%y%m")
        # 如果最新JobNo的年月和当前年月相同，则自动生成下一个JobNo
        if year_month in latest_job_no:
            cur_job_no = "RT" + str(int(latest_job_no[-6:]) + 1)
        # 否则，生成新的年月的JobNo
        else:
            cur_job_no = "RT" + year_month + "01"
        ###### 自动生成JobNo ######

        if checkout_id != 0:
            obj = get_object_or_404(TCheckouts, id=checkout_id)
            form = ScheduleForm(
                initial={
                    "JobNo": cur_job_no,
                    "PartNo": obj.PartNo,
                    "SampleSize": obj.checkout_qty,
                    "Work_Order": obj.Work_Order,
                    "StartDate": obj.checkout_date,
                }
            )
        else:
            form = ScheduleForm(
                initial={
                    "JobNo": cur_job_no,
                }
            )
        return render(request, template_name, {"title": title_text, "form": form})

    if "back" in request.POST:
        return redirect(redirect_view_name)
    data = request.POST.copy()
    form = ScheduleForm(data)
    form = deal_schedule_datas(form)
    if form.is_valid():
        form.save()
        return redirect(redirect_view_name)
    else:
        return render(request, template_name, {"title": title_text, "form": form})


def delete_schedules(request, pk):
    return handle_delete(request, TSchedule, pk, "schedules")


################# Technicians #################


def technicians(request):
    all_technicians = TTechnician.objects.all()
    context = {
        "all_technicians": all_technicians,
        "title": "测试人员管理",
    }
    return render(request, "ortplans/technicians.html", context)


def edit_technicians(request, technician_id=0):
    return render_edit_form(
        request,
        TTechnician,
        TechnicianForm,
        technician_id,
        "ortplans/edit_table1.html",
        "technicians",
        "测试人员编辑",
    )


def add_technicians(request):
    return render_add_form(
        request,
        TechnicianForm,
        "ortplans/edit_table1.html",
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
    return render(request, "ortplans/testitems.html", context)


def edit_testitems(request, testitem_id=0):
    return render_edit_form(
        request,
        TTestItem,
        TestItemForm,
        testitem_id,
        "ortplans/edit_table1.html",
        "testitems",
        "测试项目编辑",
    )


def add_testitems(request):
    return render_add_form(
        request,
        TestItemForm,
        "ortplans/edit_table1.html",
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
    return render(request, "ortplans/custproducts.html", context)


def edit_customers(request, customer_id=0):
    return render_edit_form(
        request,
        TCustCode,
        CustCodeForm,
        customer_id,
        "ortplans/edit_table1.html",
        "custproducts",
        "客户编辑",
    )


def add_customers(request):
    return render_add_form(
        request, CustCodeForm, "ortplans/edit_table1.html", "custproducts", "客户添加"
    )


def delete_customers(request, customer_id):
    return handle_delete(request, TCustCode, customer_id, "custproducts")


def edit_products(request, product_id=0):
    return render_edit_form(
        request,
        TProductType,
        ProductTypeForm,
        product_id,
        "ortplans/edit_table1.html",
        "custproducts",
        "产品编辑",
    )


def add_products(request):
    return render_add_form(
        request,
        ProductTypeForm,
        "ortplans/edit_table1.html",
        "custproducts",
        "产品添加",
    )


def delete_products(request, product_id):
    return handle_delete(request, TProductType, product_id, "custproducts")
