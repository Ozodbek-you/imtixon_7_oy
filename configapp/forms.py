from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage

from django import forms
from .models import Profile, Project, CaseStudy, BlogPost, Testimonial, ResumeItem, ContactMessage


# Profil ma'lumotlarini yangilash uchun forma
# Bu forma avatarni yangilash uchun ham ishlatiladi
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'role', 'bio', 'location', 'is_freelance_available', 'email', 'experience',
                  'projects_count']
        widgets = {
            'avatar': forms.FileInput(),
            'role': forms.TextInput(attrs={'placeholder': 'Masalan: Backend dasturchi'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Oʻzingiz haqingizda qisqacha maʼlumot...', 'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'Masalan: Oʻzbekiston'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Sizning emailingiz'}),
            'experience': forms.TextInput(attrs={'placeholder': 'Masalan: 3 yillik tajriba'}),
            'projects_count': forms.TextInput(attrs={'placeholder': 'Masalan: 15 ta loyiha'}),
        }


# Loyiha ma'lumotlarini qoʻshish/oʻzgartirish uchun forma
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'skills', 'thumbnail']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Loyiha nomi'}),
            'description': forms.Textarea(attrs={'placeholder': 'Loyiha haqida qisqacha maʼlumot...', 'rows': 3}),
            'skills': forms.TextInput(
                attrs={'placeholder': 'Masalan: Python, Django, REST API (vergul bilan ajrating)'}),
            'thumbnail': forms.FileInput(),
        }


# Case Study ma'lumotlarini qoʻshish/oʻzgartirish uchun forma
class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = ['title', 'description', 'results', 'technologies']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Case study sarlavhasi'}),
            'description': forms.Textarea(attrs={'placeholder': 'Loyiha maqsadlari...', 'rows': 3}),
            'results': forms.Textarea(
                attrs={'placeholder': 'Natijalar (har birini yangi qatordan kiriting)', 'rows': 4}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Ishlatilgan texnologiyalar'}),
        }


# Blog posti ma'lumotlarini qoʻshish/oʻzgartirish uchun forma
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'summary', 'thumbnail', 'full_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Blog post sarlavhasi'}),
            'summary': forms.Textarea(attrs={'placeholder': 'Qisqacha mazmun...', 'rows': 3}),
            'thumbnail': forms.FileInput(),
            'full_url': forms.URLInput(attrs={'placeholder': 'Blog postga toʻliq havola'}),
        }


# Fikr-mulohaza (Testimonial) qoʻshish uchun forma
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['text', 'author', 'role']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Fikr-mulohaza matni', 'rows': 3}),
            'author': forms.TextInput(attrs={'placeholder': 'Muallifning ismi'}),
            'role': forms.TextInput(attrs={'placeholder': 'Muallifning lavozimi (ixtiyoriy)'}),
        }


# Rezyume elementini qoʻshish/oʻzgartirish uchun forma
class ResumeItemForm(forms.ModelForm):
    class Meta:
        model = ResumeItem
        fields = ['title', 'company', 'duration', 'description', 'item_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Lavozim yoki taʼlim darajasi'}),
            'company': forms.TextInput(attrs={'placeholder': 'Kompaniya yoki universitet'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Masalan: 2022 — Hozirgacha'}),
            'description': forms.Textarea(attrs={'placeholder': 'Vazifalar yoki taʼlim haqida qisqacha', 'rows': 3}),
            'item_type': forms.Select(),
        }


# Aloqa formasi (siz bergan koddagi ContactForm)
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ismingiz', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@misol.com', 'required': 'required'}),
            'message': forms.Textarea(attrs={'placeholder': 'Xabaringiz...', 'required': 'required'}),
        }