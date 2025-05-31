from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, HostelApplication, University, Hostel, Room

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UniversityRegistrationForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ('name', 'location', 'contact_email', 'contact_phone')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ('name', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_number', 'room_type', 'capacity', 'available_capacity', 'floor')
        widgets = {
            'capacity': forms.NumberInput(attrs={'min': 1}),
            'available_capacity': forms.NumberInput(attrs={'min': 0}),
            'floor': forms.NumberInput(attrs={'min': 0}),
        }

    def clean(self):
        cleaned_data = super().clean()
        capacity = cleaned_data.get('capacity')
        available_capacity = cleaned_data.get('available_capacity')
        
        if capacity and available_capacity and available_capacity > capacity:
            raise forms.ValidationError("Available capacity cannot be greater than total capacity")
        
        return cleaned_data

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_id', 'phone_number', 'address', 'university')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class HostelApplicationForm(forms.ModelForm):
    student_remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = HostelApplication
        fields = ('hostel', 'room', 'student_remarks')
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['hostel'].queryset = Hostel.objects.filter(
                university=student.university
            )
            self.fields['room'].queryset = Room.objects.none()

            if 'hostel' in self.data:
                try:
                    hostel_id = int(self.data.get('hostel'))
                    self.fields['room'].queryset = Room.objects.filter(
                        hostel_id=hostel_id,
                        available_capacity__gt=0
                    )
                except (ValueError, TypeError):
                    pass 