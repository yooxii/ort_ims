from django.db import models


# Create your models here.
class TOrtReports(models.Model):
    id = models.AutoField(primary_key=True)
    Report_File = models.FileField(
        verbose_name="报告文件",
        upload_to="",
    )
