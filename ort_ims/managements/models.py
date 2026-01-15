from django.db import models

# Create your models here.


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
        default="NA",
    )
    dispose = models.CharField(
        verbose_name="样品处理",
        max_length=25,
        choices=(("回线", "回线"), ("报废", "报废")),
        default="回线",
    )
    Remark = models.TextField(
        verbose_name="备注",
        default="",
        blank=True,
    )

    def __str__(self):
        return self.test_item


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
        default="",
    )
    tech_phone = models.CharField(
        verbose_name="电话",
        max_length=20,
        default="",
    )

    def __str__(self):
        return self.tech_name
