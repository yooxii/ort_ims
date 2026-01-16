from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic

from ort_ims.common.views import handle_delete
from ort_ims.managements.models import TCustCode
from ort_ims.managements.models import TProductType
from ort_ims.managements.models import TTechnician
from ort_ims.managements.models import TTestItem
from ort_ims.plans.forms import CheckoutForm
from ort_ims.plans.forms import ScheduleForm
from ort_ims.plans.models import TCheckouts

# Create your views here.
from ort_ims.plans.models import TSchedule


def index(request):
    return render(request, "index.html")


################# Checkouts #################


class CheckoutsView(generic.ListView):
    model = TCheckouts
    template_name = "plans/checkouts.html"


def checkouts(request):
    all_checkouts = TCheckouts.objects.all()
    context = {
        "all_checkouts": all_checkouts,
    }
    return render(request, "plans/checkouts.html", context)


def import_checkouts(request):
    return render(request, "plans/import_checkouts.html")


def export_checkouts(request):
    return render(request, "plans/export_checkouts.html")


def edit_checkouts(request: HttpRequest, pk=0):
    model_class = TCheckouts
    form_class = CheckoutForm
    template_name = "plans/edit_table1.html"
    object_id = pk
    redirect_view_name = "plans:checkouts"
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
                return redirect("plans:edit_schedules", sch.id)
            return redirect("plans:add_schedules", pk=obj.id)
        return redirect(redirect_view_name)
    return render(request, template_name, {"title": title_text, "form": form})


def add_checkouts(request):
    template_name = "plans/edit_table1.html"
    form_class = CheckoutForm
    redirect_view_name = "plans:checkouts"
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
            return redirect("plans:add_schedules", pk=obj.id)
        return redirect(redirect_view_name)
    return render(request, template_name, {"title": title_text, "form": form})


def delete_checkouts(request, pk):
    return handle_delete(request, TCheckouts, pk, "plans:checkouts")


################# Schedules #################


class SchedulesView(generic.ListView):
    model = TSchedule
    template_name = "plans/schedules.html"


def import_schedules(request):
    return render(request, "plans/import_schedules.html")


def export_schedules(request):
    return render(request, "plans/export_schedules.html")


class EditSchedulesView(generic.DetailView):
    model = TSchedule
    form_class = ScheduleForm
    template_name = "plans/edit_table1.html"
    redirect_view_name = "plans:schedules"
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
                hours=float(obj_test_item.test_time),
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
            },
        )

    except (ValueError, ValidationError) as e:
        form.add_error(None, str(e))

    return form


def add_schedules(request, pk):
    template_name = "plans/edit_table1.html"
    redirect_view_name = "plans:schedules"
    title_text = "排程添加"

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

        if pk != 0:
            obj = get_object_or_404(TCheckouts, id=pk)
            form = ScheduleForm(
                initial={
                    "JobNo": cur_job_no,
                    "PartNo": obj.PartNo,
                    "SampleSize": obj.checkout_qty,
                    "Work_Order": obj.Work_Order,
                    "StartDate": obj.checkout_date,
                },
            )
        else:
            form = ScheduleForm(
                initial={
                    "JobNo": cur_job_no,
                },
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
    return render(request, template_name, {"title": title_text, "form": form})


def delete_schedules(request, pk):
    return handle_delete(request, TSchedule, pk, "plans:schedules")
