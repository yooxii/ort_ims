from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button
from crispy_forms.layout import Column
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Row
from crispy_forms.layout import Submit
from django import forms

from ort_ims.reports.models import TORTReportOverview
from ort_ims.reports.models import TORTReports


class ORTReportsForm(forms.ModelForm):
    class Meta:
        model = TORTReports
        fields = ["report_file", "report_type", "close_date", "Remark"]
        widgets = {
            "close_date": forms.DateInput(attrs={"type": "date"}, format="%Y/%m/%d"),
            "Remark": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("report_type", css_class="form-group col-md-6 mb-0"),
                Column("close_date", css_class="form-group col-md-6 mb-0"),
            ),
            Row(
                Column("report_file", css_class="form-group col-md-12 mb-0"),
            ),
            Row(
                Column("Remark", css_class="form-group col-md-12 mb-0"),
            ),
            Div(
                Submit("submit", "提交", css_class="btn btn-primary"),
            ),
        )
        super().__init__(*args, **kwargs)


class ORTReportOverviewForm(forms.ModelForm):
    class Meta:
        model = TORTReportOverview
        fields = [
            "overview_file",
        ]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("overview_file", css_class="form-group col-md-12 mb-0"),
            ),
            Div(
                Submit("submit", "提交", css_class="btn btn-primary"),
            ),
        )
