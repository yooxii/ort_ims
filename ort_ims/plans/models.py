from pathlib import Path

from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class RenameFile:
    def __init__(self, sub_path: str):
        self.path = Path(sub_path)

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # 获取当前年月
        now = timezone.now()
        year_month = now.strftime("%Y/%m")
        filename = f"{year_month}/{instance.PartNo}.{ext}"
        return self.path / filename


rename_sn_file = RenameFile("sn_files/")


class TSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    jobno = models.CharField(
        verbose_name="工作编号",
        max_length=20,
        unique=True,
    )
    QRT = models.BooleanField(
        verbose_name="送测",
        default=False,
        choices=((False, "领用"), (True, "送测")),
    )
    product = models.ForeignKey(
        verbose_name="产品类型",
        to="managements.TProductType",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    customer = models.ForeignKey(
        verbose_name="客户名称",
        to="managements.TCustCode",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    partno = models.CharField(
        verbose_name="机种名",
        max_length=15,
    )
    stage = models.IntegerField(
        verbose_name="阶段",
        default=1,
        choices=((1, "MP"), (2, "MVT"), (3, "DVT"), (4, "EVT")),
    )
    test_item = models.ForeignKey(
        verbose_name="测试项目",
        to="managements.TTestItem",
        to_field="id",
        default=29,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    qty = models.IntegerField(
        verbose_name="样品数",
        default=3,
    )
    test_period = models.IntegerField(
        verbose_name="试验时间",
    )
    owner = models.CharField(
        verbose_name="负责人",
        max_length=50,
        default="NA",
    )
    start_date = models.DateField(
        verbose_name="开始日期",
    )
    end_date = models.DateField(
        verbose_name="结束日期",
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        verbose_name="完成状态",
        default=1,
        choices=((1, "Ongoing"), (2, "Close"), (3, "Pending")),
    )
    upload_elab = models.BooleanField(
        verbose_name="上传系统",
        null=True,
        blank=True,
        default=False,
        choices=((False, "未上传"), (True, "已上传")),
    )
    workorder = models.CharField(
        verbose_name="工令",
        max_length=40,
        unique=True,
        null=True,
        blank=True,
    )
    remark = models.TextField(
        verbose_name="备注",
        default="",
        blank=True,
    )

    def __str__(self):
        return self.jobno


class TCheckouts(models.Model):
    id = models.AutoField(primary_key=True)
    checkout_date = models.DateField(
        verbose_name="领用日期",
    )
    checkout_no = models.CharField(
        verbose_name="领用单号",
        max_length=20,
        unique=True,
    )
    partno = models.CharField(
        verbose_name="机种名称",
        max_length=15,
    )
    checkout_qty = models.IntegerField(
        verbose_name="领出数量",
        default=3,
    )
    sn = models.TextField(
        verbose_name="序列号",
        blank=True,
        default="",
    )
    dc = models.CharField(
        verbose_name="周期",
        max_length=8,
    )
    rev = models.CharField(
        verbose_name="版本",
        max_length=10,
    )
    workorder = models.CharField(
        verbose_name="工令",
        max_length=40,
        unique=True,
    )
    rt_workorder = models.CharField(
        verbose_name="回线RT工令",
        max_length=40,
        null=True,
        blank=True,
    )
    return_no = models.CharField(
        verbose_name="退料单号",
        max_length=20,
        null=True,
        blank=True,
    )
    return_qty = models.IntegerField(
        verbose_name="入库数量",
        default=0,
    )
    return_date = models.DateField(
        verbose_name="入库日期",
        default=timezone.now,
    )
    status = models.IntegerField(
        verbose_name="单体状态",
        default=2,
        choices=((1, "未领用"), (2, "已领用"), (3, "已归还"), (4, "已报废")),
    )
    sn_file = models.FileField(
        verbose_name="序列号文件",
        upload_to=rename_sn_file,
        null=True,
        blank=True,
    )
    remark = models.TextField(
        verbose_name="备注",
        default="",
        blank=True,
    )

    def __str__(self):
        return self.workorder
