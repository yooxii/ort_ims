import re
from pathlib import Path

from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible


def _sanitize_path_component(component):
    """清理路径组件,移除危险字符"""
    if component is None:
        return ""
    # 转换为字符串并清理
    component = str(component).strip()
    # 移除路径遍历字符和危险字符
    component = re.sub(r'[<>:"|?*\\]', "_", component)
    # 防止路径遍历
    component = component.replace("../", "").replace("..\\", "")
    return component.replace("./", "").replace(".\\", "")


@deconstructible
class RenameFile:
    def __init__(self, parent_path: str, sub_path: str = ""):
        self.parent_path = Path(parent_path)
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # 安全地处理动态路径组件
        part_no = _sanitize_path_component(getattr(instance, "PartNo", ""))
        dc = _sanitize_path_component(getattr(instance, "dc", ""))
        job_no = _sanitize_path_component(getattr(instance, "JobNo", ""))

        # 获取年月
        make_date = getattr(instance, "make_date", timezone.now())

        prefix = f"BI EMI/{make_date.year} EMI & 168H 完成/{make_date.month}"

        # 清理文件名
        clean_filename = _sanitize_path_component(filename)

        _dir = f"{prefix}/{part_no} ORT Test Report (WK{dc})_{job_no}"
        return self.parent_path / _dir / self.sub_path / clean_filename


rename_report = RenameFile("reports/", "Report")
rename_overview = RenameFile("reports/")


# Create your models here.
class TORTReports(models.Model):
    id = models.AutoField(primary_key=True)
    JobNo = models.ForeignKey(
        to="plans.TSchedule",
        to_field="JobNo",
        verbose_name="工作编号",
        on_delete=models.CASCADE,
    )
    PartNo = models.CharField(
        verbose_name="机种名称",
        max_length=15,
    )
    dc = models.CharField(
        verbose_name="周期",
        max_length=8,
    )
    report_type = models.ForeignKey(
        to="managements.TTestItem",
        to_field="test_item",
        verbose_name="测试类型",
        on_delete=models.RESTRICT,
    )
    report_file = models.FileField(
        verbose_name="报告文件",
        upload_to=rename_report,
        unique=True,
    )
    make_date = models.DateField(
        verbose_name="创建日期",
    )
    close_date = models.DateField(
        verbose_name="完成日期",
    )
    Remark = models.TextField(
        verbose_name="备注",
        default="",
    )

    def __str__(self):
        return self.report_file.name


class TORTReportOverview(models.Model):
    id = models.AutoField(primary_key=True)
    JobNo = models.ForeignKey(
        to="plans.TSchedule",
        to_field="JobNo",
        verbose_name="工作编号",
        on_delete=models.CASCADE,
    )
    PartNo = models.CharField(
        verbose_name="机种名称",
        max_length=15,
    )
    dc = models.CharField(
        verbose_name="周期",
        max_length=8,
    )
    overview_file = models.FileField(
        verbose_name="报告总览",
        upload_to=rename_overview,
        unique=True,
    )
    make_date = models.DateField(
        verbose_name="创建日期",
    )

    def __str__(self):
        return self.overview_file.name
