from django import forms

from .models import Client
from .validators import validate_phone_number

_INPUT = (
    'mt-1.5 block w-full rounded-lg border border-zinc-600 bg-zinc-800/50 '
    'px-4 py-3 text-white placeholder-zinc-500 focus:border-accent-cyan '
    'focus:outline-none focus:ring-1 focus:ring-accent-cyan sm:text-sm'
)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'phone_number',
            'city',
            'gender',
            'age',
            'height',
            'weight',
            'goal',
            'program_name',
            'program_start_date',
            'program_end_date',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'name'}),
            'phone_number': forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'tel'}),
            'city': forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'address-level2'}),
            'gender': forms.Select(attrs={'class': _INPUT}),
            'age': forms.NumberInput(attrs={'class': _INPUT, 'min': 1}),
            'height': forms.NumberInput(attrs={'class': _INPUT, 'min': 0, 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'class': _INPUT, 'min': 0, 'step': '0.01'}),
            'goal': forms.Select(attrs={'class': _INPUT}),
            'program_name': forms.TextInput(attrs={'class': _INPUT}),
            'program_start_date': forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'program_end_date': forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
        }



class ClientInvitationForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label='Full Name',
        widget=forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'name'}),
    )
    phone_number = forms.CharField(
        max_length=20,
        validators=[validate_phone_number],
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'tel', 'inputmode': 'tel'}),
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label='City',
        widget=forms.TextInput(attrs={'class': _INPUT, 'autocomplete': 'address-level2'}),
    )
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        label='Gender',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        label='Age',
        widget=forms.NumberInput(attrs={'class': _INPUT, 'min': 1}),
    )
    height = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label='Height (cm)',
        widget=forms.NumberInput(attrs={'class': _INPUT, 'min': 0, 'step': '0.01'}),
    )
    weight = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={'class': _INPUT, 'min': 0, 'step': '0.01'}),
    )
    goal = forms.ChoiceField(choices=[
        ('CUT', 'Fat Loss'),
        ('BULK', 'Muscle Gain'),
        ('MAINTAIN', 'Maintenance'),
        ('ATHLETIC', 'Athletic Performance'),
    ], label='Goal', widget=forms.Select(attrs={'class': _INPUT}))