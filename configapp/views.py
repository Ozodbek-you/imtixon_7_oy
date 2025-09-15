from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import  UserProfileForm, UserLoginForm
from django.http import FileResponse, Http404, HttpResponse
import os
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .forms import ContactForm
from .models import ContactMessage

# Footer form orqali xabar yuborish
def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi ✅")
            return redirect("base")  # home sahifaga qaytariladi
    else:
        form = ContactForm()
    return render(request, "base.html", {"contact_form": form})


# Xabarlarni ko‘rish (faqat adminlar uchun)
@login_required
def contact(request):
    if not request.user.is_staff:  # faqat admin/staff ko‘ra oladi
        messages.error(request, "Sizda ruxsat yo‘q ❌")
        return redirect("base")

    messages_list = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "contact.html", {"messages": messages_list})


def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50  # Start position from the top
    styles = getSampleStyleSheet()

    # Function to add a new page if needed
    def new_page_if_needed(current_y, margin=50):
        nonlocal p
        if current_y < margin:
            p.showPage()
            p.setFillColor(HexColor("#0f1724"))
            p.rect(0, 0, width, height, fill=1)
            return height - 50
        return current_y

    # Background
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    # Header - Backend Developerga moslashtirildi
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, "Salom, men Ozodbek — Backend Developer")
    y -= 30

    # Lead Text - Backendga moslashtirildi
    y = new_page_if_needed(y)
    lead_text = ("Men zamonaviy, performansga yo‘naltirilgan backend tizimlar yarataman — "
                 "REST API, mikroservislar, ma'lumotlar bazasi integratsiyasi va optimizatsiya. "
                 "Portfolioim loyihalarimning eng yaxshi backend yechimlarini taqdim etadi.")
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 12
    style.textColor = HexColor("#cfeef4")
    p_obj = Paragraph(lead_text, style)
    w, h = p_obj.wrap(width - 80, y)  # width - 80 chunki 40 margin har tomondan
    p_obj.drawOn(p, 40, y - h)
    y -= h + 20

    # Skills
    y = new_page_if_needed(y)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Ko‘nikmalar:")
    y -= 20

    skills = ["Python", "Django", "REST API", "PostgreSQL", "Docker", "Celery", "Redis", "Testing"]
    for skill in skills:
        y = new_page_if_needed(y)
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(50, y, f"- {skill}")
        y -= 15
    y -= 10

    # Projects
    y = new_page_if_needed(y)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Loyihalar:")
    y -= 20

    projects = [
        ("TaskApp API", "ToDo & Task Manager backend - API bilan foydalanuvchi vazifalarini boshqarish."),
        ("Blog CMS Backend", "RESTful API va ma'lumotlar bazasi bilan blog platformasi yaratildi."),
        ("Auto Detailing Backend",
         "Ma'lumotlar bazasi va fayl serverni optimizatsiya qilish, lazy-loading bilan tasvirlar xizmatini yaratish.")
    ]

    for title, desc in projects:
        y = new_page_if_needed(y)
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(50, y, f"{title}:")
        y -= 15
        # Description as Paragraph
        style.fontSize = 11
        p_obj = Paragraph(desc, style)
        w, h = p_obj.wrap(width - 100, y)
        p_obj.drawOn(p, 60, y - h)
        y -= h + 15

    # Case Studies
    y = new_page_if_needed(y)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Case Studies:")
    y -= 20

    case_studies = [
        ("Case: TaskApp API Optimization",
         "Maqsad: API javob vaqtini kamaytirish va parallel so‘rovlarni qo‘llab-quvvatlash. Natija: response time 0.3s gacha qisqardi."),
        ("Case: Blog CMS Backend Scaling",
         "Maqsad: ko‘p foydalanuvchi kirishini qo‘llab-quvvatlash. Natija: Load testingda 10,000 so‘rov/sekund muvaffaqiyatli bajarildi.")
    ]

    for title, desc in case_studies:
        y = new_page_if_needed(y)
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(50, y, f"{title}")
        y -= 15
        # Description as Paragraph
        style.fontSize = 11
        p_obj = Paragraph(desc, style)
        w, h = p_obj.wrap(width - 100, y)
        p_obj.drawOn(p, 60, y - h)
        y -= h + 15

    # Finalize PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")

def base_view(request):
    return render(request, "base.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_views(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Xush kelibsiz, " + username + "!")
                return redirect("base")
            else:
                messages.error(request, "Login yoki parol xato!")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("login")




