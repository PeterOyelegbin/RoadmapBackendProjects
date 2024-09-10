from django.forms import ModelForm, FileInput
from .models import MarkDown

# Create your forms here.
class MarkDownForm(ModelForm):
    class Meta:
        model = MarkDown
        fields = ["file"]
        labels = {
            "file": "Upload a Markdown file (e.g; .md)",
        }
        widgets = {
            "file": FileInput(attrs={"class":"form-control"}),
        }
