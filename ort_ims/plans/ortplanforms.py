from django import forms
from ort_ims.plans.models import TProductType, TCustCode, TSchedule, TCheckouts, TTestItem, TTechnician
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field, Button


class CustCodeForm(forms.ModelForm):
    class Meta:
        model = TCustCode
        fields = [
            "cust_code",
            "cust_name",
        ]

    def __init__(self, *args, **kwargs):
        super(CustCodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("cust_code", css_class="form-group col-md-2 mb-0"),
                Column("cust_name", css_class="form-group col-md-1 mb-0"),
                css_class="form-row",
            ),
            Div(
                Submit(
                    "返回", "返回", css_class="button white", onclick="history.back(-1)"
                ),
                Submit("保存", "保存", css_class="button white"),
            ),
        )


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = TTechnician
        fields = [
            "tech_code",
            "tech_name",
            "tech_email",
            "tech_phone",
        ]

    def __init__(self, *args, **kwargs):
        super(TechnicianForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("tech_code", css_class="form-group col-md-6 mb-0"),
                Column("tech_name", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("tech_email", css_class="form-group col-md-6 mb-0"),
                Column("tech_phone", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Div(
                Submit(
                    "返回", "返回", css_class="button white", onclick="history.back(-1)"
                ),
                Submit("保存", "保存", css_class="button white"),
            ),
        )


class TestItemForm(forms.ModelForm):
    class Meta:
        model = TTestItem
        fields = [
            "test_item",
            "test_time",
            "test_owner",
            "dispose",
            "Remark",
        ]

    def __init__(self, *args, **kwargs):
        super(TestItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("test_item", css_class="form-group col-md-3 mb-0"),
                Column("test_time", css_class="form-group col-md-3 mb-0"),
                Column("dispose", css_class="form-group col-md-3 mb-0"),
                Column("test_owner", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("Remark", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            Div(
                Submit(
                    "返回", "返回", css_class="button white", onclick="history.back(-1)"
                ),
                Submit("保存", "保存", css_class="button white"),
            ),
        )


class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = TProductType
        fields = [
            "product_code",
            "product_type",
        ]

    def __init__(self, *args, **kwargs):
        super(ProductTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("product_code", css_class="form-group col-md-2 mb-0"),
                Column("product_type", css_class="form-group col-md-1 mb-0"),
                css_class="form-row",
            ),
            Div(
                Submit(
                    "返回", "返回", css_class="button white", onclick="history.back(-1)"
                ),
                Submit("保存", "保存", css_class="button white"),
            ),
        )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = TCheckouts
        fields = [
            "checkout_no",
            "PartNo",
            "checkout_date",
            "DC",
            "checkout_qty",
            "REV",
            "Work_Order",
            "checkout_status",
            "SN",
            "Remarks",
            "sn_file",
        ]
        widgets = {
            "checkout_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "SN": forms.Textarea(attrs={"rows": 5}),
            "Remarks": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("checkout_no", css_class="form-group col-md-3 mb-0"),
                Column("PartNo", css_class="form-group col-md-3 mb-0"),
                Column("checkout_date", css_class="form-group col-md-3 mb-0"),
                Column("DC", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("checkout_qty", css_class="form-group col-md-3 mb-0"),
                Column("REV", css_class="form-group col-md-3 mb-0"),
                Column("Work_Order", css_class="form-group col-md-3 mb-0"),
                Column("checkout_status", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("SN", css_class="form-group col-md-6 mb-0"),
                Column("sn_file", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("Remarks", css_class="form-group col-md-12 mb-0"),
                css_class="form-row",
            ),
            Div(
                Button(
                    "back",
                    "返回",
                    css_class="btn btn-secondary",
                    onclick="location.href='/ORTplans/checkouts'",
                ),
                Submit("save", "保存", css_class="button white"),
                Submit(
                    "save_and_schedule",
                    "保存并转到排程编辑",
                    css_class="button white",
                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        sn_file = cleaned_data.get("sn_file")
        sn = cleaned_data.get("SN")
        if not sn_file and not sn:
            raise forms.ValidationError("请上传SN文件或输入SN信息")
        if sn_file:
            cleaned_data["SN"] = ""
        return cleaned_data


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = TSchedule
        fields = [
            "JobNo",
            "QRT",
            "Product",
            "Customer",
            "PartNo",
            "Stage",
            "TestItem",
            "SampleSize",
            "TestPeriod",
            "Owner",
            "StartDate",
            "EndDate",
            "Status",
            "Upload_Elab",
            "Work_Order",
            "Remark",
        ]
        widgets = {
            "StartDate": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "EndDate": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "Remark": forms.Textarea(attrs={"rows": 3, "cols": 30}),
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("JobNo", css_class="form-group col-md-1 mb-0"),
                Column("QRT", css_class="form-group col-md-1 mb-0"),
                Column("PartNo", css_class="form-group col-md-2 mb-0"),
                Column("Stage", css_class="form-group col-md-1 mb-0"),
                Column("SampleSize", css_class="form-group col-md-1 mb-0"),
                Column("TestItem", css_class="form-group col-md-3 mb-0"),
                Column("Work_Order", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("StartDate", css_class="form-group col-md-3 mb-0"),
                Column("EndDate", css_class="form-group col-md-3 mb-0"),
                Column("Status", css_class="form-group col-md-3 mb-0"),
                Column("Upload_Elab", css_class="form-group col-md-3 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("Remark", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Div(
                Button(
                    "back",
                    "返回",
                    css_class="btn btn-secondary",
                    onclick="location.href='/ORTplans/schedules'",
                ),
                Submit("save", "保存", css_class="button white"),
            ),
        )
