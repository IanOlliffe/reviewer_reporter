from django import forms
from plugins.reporting import forms as reporting_forms 

class ReviewerReporterForm(forms.Form):
    start_date = reporting_forms.DateForm.base_fields['start_date']
    end_date = reporting_forms.DateForm.base_fields['end_date']
