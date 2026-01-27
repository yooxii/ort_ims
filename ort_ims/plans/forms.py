from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import Column
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Row
from crispy_forms.layout import Submit
from django import forms

from ort_ims.plans.models import TCheckouts
from ort_ims.plans.models import TSchedule


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = TCheckouts
        fields = [
            "checkout_date",
            "checkout_no",
            "partno",
            "checkout_qty",
            "sn",
            "dc",
            "rev",
            "workorder",
            "rt_workorder",
            "return_no",
            "return_qty",
            "return_date",
            "status",
            "sn_file",
            "remark",
        ]
        widgets = {
            "checkout_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "sn": forms.Textarea(attrs={"rows": 5}),
            "remark": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("checkout_no", css_class="form-group col-md-3 mb-0"),
                Column("partno", css_class="form-group col-md-3 mb-0"),
                Column("checkout_date", css_class="form-group col-md-3 mb-0"),
                Column("dc", css_class="form-group col-md-3 mb-0"),
            ),
            Row(
                Column("checkout_qty", css_class="form-group col-md-3 mb-0"),
                Column("rev", css_class="form-group col-md-3 mb-0"),
                Column("workorder", css_class="form-group col-md-3 mb-0"),
                Column("status", css_class="form-group col-md-3 mb-0"),
            ),
            Row(
                Column("rt_workorder", css_class="form-group col-md-3 mb-0"),
                Column("return_no", css_class="form-group col-md-3 mb-0"),
                Column("return_qty", css_class="form-group col-md-3 mb-0"),
                Column("return_date", css_class="form-group col-md-3 mb-0"),
            ),
            Row(
                Column("sn", css_class="form-group col-md-6 mb-0"),
                Column("sn_file", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("remark", css_class="form-group col-md-12 mb-0"),
            ),
            Div(
                Button(
                    "back",
                    "返回",
                    css_class="btn btn-secondary",
                    onclick="location.href='/plans/checkouts'",
                ),
                Submit("save", "保存", css_class="button white"),
                Submit(
                    "save_and_schedule",
                    "保存并转到排程编辑",
                    css_class="button white",
                ),
                css_class="row mb-5 pl-3 text-right",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        sn_file = cleaned_data.get("sn_file")
        sn = cleaned_data.get("sn")
        if not sn_file and not sn:
            msg = "请上传SN文件或输入SN信息"
            raise forms.ValidationError(msg)
        if sn_file:
            cleaned_data["sn"] = ""
        return cleaned_data


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = TSchedule
        fields = [
            "jobno",
            "QRT",
            "product",
            "customer",
            "partno",
            "stage",
            "test_item",
            "qty",
            "test_period",
            "owner",
            "start_date",
            "end_date",
            "status",
            "upload_elab",
            "workorder",
            "remark",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remark": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("jobno", css_class="form-group col-md-1 mb-0"),
                Column("QRT", css_class="form-group col-md-1 mb-0"),
                Column("partno", css_class="form-group col-md-2 mb-0"),
                Column("stage", css_class="form-group col-md-1 mb-0"),
                Column("qty", css_class="form-group col-md-1 mb-0"),
                Column("test_item", css_class="form-group col-md-3 mb-0"),
                Column("workorder", css_class="form-group col-md-3 mb-0"),
            ),
            Row(
                Column("start_date", css_class="form-group col-md-3 mb-0"),
                Column("end_date", css_class="form-group col-md-3 mb-0"),
                Column("status", css_class="form-group col-md-3 mb-0"),
                Column("upload_elab", css_class="form-group col-md-3 mb-0"),
            ),
            Row(
                Column("remark", css_class="form-group col-md-5 mb-0"),
            ),
            Div(
                Button(
                    "back",
                    "返回",
                    css_class="btn btn-secondary",
                    onclick="location.href='/plans/schedules'",
                ),
                Submit("save", "保存", css_class="button white"),
            ),
        )
