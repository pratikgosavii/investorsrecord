from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class investor_Form(forms.ModelForm):
    class Meta:
        model = investor
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'address'
            }),

            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),

            'remark': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'remark'
            }),

            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
            
        }



from django import forms
from .models import operator
from users.models import User

class operator_Form(forms.ModelForm):
    username = forms.CharField(
        max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username'})
    )
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'})
    )

    class Meta:
        model = operator
        fields = ['name', 'address', 'mobile_no', 'remark', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address'}),
            'mobile_no': forms.NumberInput(attrs={'class': 'form-control', 'id': 'mobile_no'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'id': 'remark'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
        }

    def __init__(self, *args, **kwargs):
        super(operator_Form, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # If editing existing operator
            self.fields['username'].initial = self.instance.user.username  # Set initial username

    def save(self, commit=True):
        # Use the existing user if the operator is being updated
        if self.instance and self.instance.pk:
            user = self.instance.user
            user.username = self.cleaned_data['username']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
        else:
            # Create a new user for new operator
            user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'], is_operator = True)
        
        # Save the operator with the associated user
        operator_instance = super().save(commit=False)
        operator_instance.user = user
        if commit:
            operator_instance.save()
        return operator_instance




class transactions_Form(forms.ModelForm):

    timestamp = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control dateclas',
            'type': 'datetime-local'  # Allows both date and time input
        }),
        required=False,  # Set this to False if you don't want it to be a required field
        input_formats=['%Y-%m-%dT%H:%M']  # This format is compatible with 'datetime-local' input
    )

    def __init__(self, *args, **kwargs):
        super(transactions_Form, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # If editing existing operator
            self.fields['timestamp'].initial = self.instance.timestamp  # Set initial date_time if available

    class Meta:
        model = transactions
        fields = '__all__'
        widgets = {
            'operator': forms.Select(attrs={'class': 'form-control', 'id': 'operator'}),
            'investor': forms.Select(attrs={'class': 'form-control', 'id': 'investor'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'id': 'amount'}),
            'remark': forms.TextInput(attrs={'class': 'form-control', 'id': 'remark'}),
        }
