import os
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.deconstruct import deconstructible

from datetime import datetime, timedelta


@deconstructible
class RenameSNFile(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # 获取当前年月
        now = datetime.now()
        year_month = now.strftime("%Y/%m")
        filename = "{}/{}.{}".format(year_month, instance.PartNo, ext)
        return os.path.join(self.path, filename)


rename_sn_file = RenameSNFile("sn_files/")


class TProductType(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(
        verbose_name="产品代码",
        max_length=10,
        unique=True,
    )
    product_type = models.CharField(
        verbose_name="产品类型",
        max_length=20,
    )

    def __str__(self):
        return self.product_type



class TCustCode(models.Model):
    id = models.AutoField(primary_key=True)
    cust_code = models.CharField(
        verbose_name="客户代码",
        max_length=10,
        unique=True,
    )
    cust_name = models.CharField(
        verbose_name="客户名称",
        max_length=50,
    )

    def __str__(self):
        return self.cust_name


class TTechnician(models.Model):
    id = models.AutoField(primary_key=True)
    tech_code = models.CharField(
        verbose_name="工号",
        max_length=10,
        unique=True,
    )
    tech_name = models.CharField(
        verbose_name="姓名",
        max_length=50,
    )
    tech_email = models.EmailField(
        verbose_name="邮箱",
        null=True,
        blank=True,
    )
    tech_phone = models.CharField(
        verbose_name="电话",
        max_length=20,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.tech_name


class TTestItem(models.Model):
    id = models.AutoField(primary_key=True)
    test_item = models.CharField(
        verbose_name="测试项目",
        max_length=50,
        unique=True,
    )
    test_time = models.FloatField(
        verbose_name="测试时间(h)",
    )
    test_owner = models.CharField(
        verbose_name="测试负责人",
        max_length=50,
        null=True,
        blank=True,
    )
    dispose = models.CharField(
        verbose_name="样品处理",
        max_length=25,
        choices=(("回线", "回线"), ("报废", "报废")),
        null=True,
        blank=True,
    )
    Remark = models.TextField(verbose_name="备注", null=True, blank=True)

    def __str__(self):
        return self.test_item


class TSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    JobNo = models.CharField(
        verbose_name="工作编号",
        max_length=20,
        unique=True,
    )
    QRT = models.BooleanField(
        verbose_name="送测",
        default=False,
        choices=((False, "领用"), (True, "送测")),
    )
    Product = models.ForeignKey(
        verbose_name="产品类型",
        to="TProductType",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    Customer = models.ForeignKey(
        verbose_name="客户名称",
        to="TCustCode",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    PartNo = models.CharField(
        verbose_name="机种名",
        max_length=15,
    )
    Stage = models.IntegerField(
        verbose_name="阶段",
        default=1,
        choices=((1, "MP"), (2, "MVT"), (3, "DVT"), (4, "EVT")),
    )
    TestItem = models.ForeignKey(
        verbose_name="测试项目",
        to="TTestItem",
        to_field="id",
        default=29,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    SampleSize = models.IntegerField(
        verbose_name="样品数",
        default=3,
    )
    TestPeriod = models.IntegerField(
        verbose_name="试验时间",
    )
    Owner = models.CharField(
        verbose_name="负责人",
        null=True,
        blank=True,
        max_length=50,
    )
    StartDate = models.DateField(
        verbose_name="开始日期",
    )
    EndDate = models.DateField(
        verbose_name="结束日期",
        null=True,
        blank=True,
    )
    Status = models.IntegerField(
        verbose_name="完成状态",
        default=1,
        choices=((1, "Ongoing"), (2, "Close"), (3, "Pending")),
    )
    Upload_Elab = models.BooleanField(
        verbose_name="上传系统",
        null=True,
        blank=True,
        default=False,
        choices=((False, "未上传"), (True, "已上传")),
    )
    Work_Order = models.CharField(
        verbose_name="工令",
        max_length=40,
        unique=True,
        null=True,
        blank=True,
    )
    Remark = models.TextField(
        verbose_name="备注",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.JobNo


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
    PartNo = models.CharField(
        verbose_name="机种名称",
        max_length=15,
    )
    checkout_qty = models.IntegerField(
        verbose_name="领出数量",
    )
    SN = models.TextField(
        verbose_name="序列号",
        null=True,
        blank=True,
    )
    DC = models.CharField(
        verbose_name="周期",
        max_length=8,
    )
    REV = models.CharField(
        verbose_name="版本",
        max_length=10,
    )
    Work_Order = models.CharField(
        verbose_name="工令",
        max_length=40,
        unique=True,
    )
    Remarks = models.TextField(
        verbose_name="备注",
        null=True,
        blank=True,
    )
    checkout_status = models.IntegerField(
        verbose_name="领出状态",
        null=True,
        blank=True,
        default=2,
        choices=((1, "未领用"), (2, "已领用"), (3, "已归还")),
    )
    sn_file = models.FileField(
        verbose_name="序列号文件",
        upload_to=rename_sn_file,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.Work_Order
