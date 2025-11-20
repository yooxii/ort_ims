from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Field

from ort_ims.managements.models import (
    TTechnician,
    TProductType,
    TCustCode,
    TTestItem,
)


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


class TechnicianForm(forms.ModelForm):
    class Meta:
        model = TTechnician
        fields = ["tech_code", "tech_name", "tech_email", "tech_phone"]

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
