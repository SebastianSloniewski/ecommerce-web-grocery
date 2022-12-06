from django import forms
from cities_light.models import City


class CheckoutForm(forms.Form):
    name = forms.CharField(
        label="Imię",
    )

    surname = forms.CharField(
        label="Nazwisko"
    )

    street_address = forms.CharField(
        label = "ulica",
        widget=forms.TextInput(attrs={'placeholder': "Plac Grunwaldzki"})
    )
    building_address = forms.CharField(
        label = "nr budynku",
        widget=forms.TextInput(attrs={'placeholder': "10"})
    )
    apartment_address = forms.CharField(
        required=False,
        label = "nr mieszkania",
        widget=forms.TextInput(attrs={'placeholder': "3"})
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        to_field_name="name",
        widget=forms.Select(attrs={
            'class': 'custom-select w-100',
        })
    )
    

    postal_code = forms.CharField(
        label = "Kod pocztowy",
        widget=forms.TextInput(attrs={'placeholder': "50-315"})
    )
    
    phone_number= forms.CharField(
        max_length=9,
        label = "Numer telefonu",
        widget=forms.TextInput(attrs={'placeholder': "+48"})
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': "Jan_Kowalski@gmail.com"})
    )