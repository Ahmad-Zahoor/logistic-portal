from django import forms


class POUploadForm(forms.Form):
    file = forms.FileField(
        label="POs sheet (CSV)",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv"}),
    )

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        if not uploaded.name.lower().endswith(".csv"):
            raise forms.ValidationError("Please upload a .csv file exported from your POs sheet.")
        return uploaded
