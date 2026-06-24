from django import forms

from .models import ReservationRequest


class ReservationRequestForm(forms.ModelForm):
    class Meta:
        model = ReservationRequest
        fields = ["name", "email", "phone", "check_in", "check_out", "guests", "room", "message"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")
        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out", "Check-out date must be after check-in date.")
        return cleaned
