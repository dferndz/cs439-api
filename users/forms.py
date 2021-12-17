from django import forms


class RegisterStudentForm(forms.Form):
    eid = forms.CharField(max_length=512)
    first_name = forms.CharField(max_length=512)
    last_name = forms.CharField(max_length=512)
