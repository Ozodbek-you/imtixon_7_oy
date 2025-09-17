from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
# from .forms import  UserProfileForm, UserLoginForm
from django.http import FileResponse, Http404, HttpResponse
import os
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .forms import ContactForm, ProjectForm, ProfileForm
from .models import ContactMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .models import Post
# from .forms import PostForm


def index(request):
    try:
        # Foydalanuvchi profilini olish (bu yerda siz login tizimini ishga tushirsangiz, request.user.profile dan foydalanasiz)
        # Hozircha oddiyroq bo'lishi uchun birinchi profilni olamiz.
        profile = Profile.objects.first()

        context = {
            'user': profile,
            'portfolio': Project.objects.filter(profile=profile) if profile else [],
            'case_studies': CaseStudy.objects.filter(profile=profile) if profile else [],
            'blog_posts': BlogPost.objects.filter(profile=profile) if profile else [],
            'testimonials': Testimonial.objects.filter(profile=profile) if profile else [],
            'resume_items': ResumeItem.objects.filter(profile=profile) if profile else [],
            'contact_form': ContactForm(),
        }
    except Profile.DoesNotExist:
        context = {
            'user': None,
            'portfolio': [],
            'case_studies': [],
            'blog_posts': [],
            'testimonials': [],
            'resume_items': [],
            'contact_form': ContactForm(),
        }

    # Aloqa formasini qayta ishlash
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi ✅")
            return redirect('base')
        else:
            messages.error(request, "Xabarni yuborishda xatolik yuz berdi. Iltimos, ma'lumotlarni tekshiring.")
            return redirect('base')

    return render(request, "base.html", context)


# Login funksiyasi
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {username}!")
                # Admin panelga yo'naltirish
                return redirect("admin_panel")
            else:
                messages.error(request, "Login yoki parol xato!")
        else:
            messages.error(request, "Noto'g'ri ma'lumotlar kiritildi.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


# Logout funksiyasi
def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("base")


# Foydalanuvchi CV-sini yuklab olish
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50  # Boshlang'ich pozitsiya
    styles = getSampleStyleSheet()

    # Yangi sahifa qo'shish funksiyasi
    def new_page_if_needed(current_y, margin=50):
        nonlocal p
        if current_y < margin:
            p.showPage()
            p.setFillColor(HexColor("#0f1724"))
            p.rect(0, 0, width, height, fill=1)
            return height - 50
        return current_y

    # Fon
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    # Yuqori qism - Backend Developerga moslab
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, "Salom, men Ozodbek — Backend Developer")
    y -= 30

    # Kirish matni
    y = new_page_if_needed(y)
    lead_text = ("Men zamonaviy, performansga yo‘naltirilgan backend tizimlar yarataman — "
                 "REST API, mikroservislar, ma'lumotlar bazasi integratsiyasi va optimizatsiya. "
                 "Portfolioim loyihalarimning eng yaxshi backend yechimlarini taqdim etadi.")
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 12
    style.textColor = HexColor("#cfeef4")
    p_obj = Paragraph(lead_text, style)
    w, h = p_obj.wrap(width - 80, y)
    p_obj.drawOn(p, 40, y - h)
    y -= h + 20

    # Ko'nikmalar
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

    # Loyihalar
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
        p.setFillColor(HexColor("#f9fafb"))
        p.drawString(50, y, f"{title}:")
        y -= 15
        style.fontSize = 11
        p_obj = Paragraph(desc, style)
        w, h = p_obj.wrap(width - 100, y)
        p_obj.drawOn(p, 60, y - h)
        y -= h + 15

    # Case Studies
    y = new_page_if_needed(y)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#f9fafb"))
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
        p.setFillColor(HexColor("#f9fafb"))
        p.drawString(50, y, f"{title}")
        y -= 15
        style.fontSize = 11
        p_obj = Paragraph(desc, style)
        w, h = p_obj.wrap(width - 100, y)
        p_obj.drawOn(p, 60, y - h)
        y -= h + 15

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")


# Admin paneli (faqat login qilgan foydalanuvchilar uchun)
@login_required
def admin(request):
    return render(request, 'admin_panel.html')

# Admin paneli
@login_required
def admin(request):
    return render(request, 'admin_panel.html')

# Projects CRUD
@login_required
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha muvaffaqiyatli qo‘shildi ✅")
            return redirect('projects_list')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@login_required
def edit_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha muvaffaqiyatli tahrirlandi ✅")
            return redirect('projects_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    messages.success(request, "Loyiha muvaffaqiyatli o‘chirildi ✅")
    return redirect('projects_list')

# Messages
@login_required
def message_list(request):
    messages_list = ContactMessage.objects.all()
    return render(request, 'message_list.html', {'messages': messages_list})

# Edit profile
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi ✅")
            return redirect('admin_panel')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
# # Footer form orqali xabar yuborish
# def contact_form(request):
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Xabaringiz muvaffaqiyatli yuborildi ✅")
#             return redirect("base")  # home sahifaga qaytariladi
#     else:
#         form = ContactForm()
#     return render(request, "base.html", {"contact_form": form})
#
#
# # Xabarlarni ko‘rish (faqat adminlar uchun)
# @login_required
# def contact(request):
#     if not request.user.is_staff:  # faqat admin/staff ko‘ra oladi
#         messages.error(request, "Sizda ruxsat yo‘q ❌")
#         return redirect("base")
#
#     messages_list = ContactMessage.objects.all().order_by("-created_at")
#     return render(request, "contact.html", {"messages": messages_list})
#
#
# def download_cv(request):
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4
#     y = height - 50  # Start position from the top
#     styles = getSampleStyleSheet()
#
#     # Function to add a new page if needed
#     def new_page_if_needed(current_y, margin=50):
#         nonlocal p
#         if current_y < margin:
#             p.showPage()
#             p.setFillColor(HexColor("#0f1724"))
#             p.rect(0, 0, width, height, fill=1)
#             return height - 50
#         return current_y
#
#     # Background
#     p.setFillColor(HexColor("#0f1724"))
#     p.rect(0, 0, width, height, fill=1)
#
#     # Header - Backend Developerga moslashtirildi
#     p.setFont("Helvetica-Bold", 24)
#     p.setFillColor(HexColor("#6EE7B7"))
#     p.drawString(40, y, "Salom, men Ozodbek — Backend Developer")
#     y -= 30
#
#     # Lead Text - Backendga moslashtirildi
#     y = new_page_if_needed(y)
#     lead_text = ("Men zamonaviy, performansga yo‘naltirilgan backend tizimlar yarataman — "
#                  "REST API, mikroservislar, ma'lumotlar bazasi integratsiyasi va optimizatsiya. "
#                  "Portfolioim loyihalarimning eng yaxshi backend yechimlarini taqdim etadi.")
#     style = styles["Normal"]
#     style.fontName = "Helvetica"
#     style.fontSize = 12
#     style.textColor = HexColor("#cfeef4")
#     p_obj = Paragraph(lead_text, style)
#     w, h = p_obj.wrap(width - 80, y)  # width - 80 chunki 40 margin har tomondan
#     p_obj.drawOn(p, 40, y - h)
#     y -= h + 20
#
#     # Skills
#     y = new_page_if_needed(y)
#     p.setFont("Helvetica-Bold", 14)
#     p.setFillColor(HexColor("#60A5FA"))
#     p.drawString(40, y, "Ko‘nikmalar:")
#     y -= 20
#
#     skills = ["Python", "Django", "REST API", "PostgreSQL", "Docker", "Celery", "Redis", "Testing"]
#     for skill in skills:
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica", 12)
#         p.setFillColor(HexColor("#e6eef8"))
#         p.drawString(50, y, f"- {skill}")
#         y -= 15
#     y -= 10
#
#     # Projects
#     y = new_page_if_needed(y)
#     p.setFont("Helvetica-Bold", 14)
#     p.setFillColor(HexColor("#60A5FA"))
#     p.drawString(40, y, "Loyihalar:")
#     y -= 20
#
#     projects = [
#         ("TaskApp API", "ToDo & Task Manager backend - API bilan foydalanuvchi vazifalarini boshqarish."),
#         ("Blog CMS Backend", "RESTful API va ma'lumotlar bazasi bilan blog platformasi yaratildi."),
#         ("Auto Detailing Backend",
#          "Ma'lumotlar bazasi va fayl serverni optimizatsiya qilish, lazy-loading bilan tasvirlar xizmatini yaratish.")
#     ]
#
#     for title, desc in projects:
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica-Bold", 12)
#         p.setFillColor(HexColor("#f9fafb"))
#         p.drawString(50, y, f"{title}:")
#         y -= 15
#         # Description as Paragraph
#         style.fontSize = 11
#         p_obj = Paragraph(desc, style)
#         w, h = p_obj.wrap(width - 100, y)
#         p_obj.drawOn(p, 60, y - h)
#         y -= h + 15
#
#     # Case Studies
#     y = new_page_if_needed(y)
#     p.setFont("Helvetica-Bold", 14)
#     p.setFillColor(HexColor("#f9fafb"))
#     p.drawString(40, y, "Case Studies:")
#     y -= 20
#
#     case_studies = [
#         ("Case: TaskApp API Optimization",
#          "Maqsad: API javob vaqtini kamaytirish va parallel so‘rovlarni qo‘llab-quvvatlash. Natija: response time 0.3s gacha qisqardi."),
#         ("Case: Blog CMS Backend Scaling",
#          "Maqsad: ko‘p foydalanuvchi kirishini qo‘llab-quvvatlash. Natija: Load testingda 10,000 so‘rov/sekund muvaffaqiyatli bajarildi.")
#     ]
#
#     for title, desc in case_studies:
#         y = new_page_if_needed(y)
#         p.setFont("Helvetica-Bold", 12)
#         p.setFillColor(HexColor("#f9fafb"))
#         p.drawString(50, y, f"{title}")
#         y -= 15
#         # Description as Paragraph
#         style.fontSize = 11
#         p_obj = Paragraph(desc, style)
#         w, h = p_obj.wrap(width - 100, y)
#         p_obj.drawOn(p, 60, y - h)
#         y -= h + 15
#
#     # Finalize PDF
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#
#     return FileResponse(buffer, as_attachment=True, filename="cv.pdf")
#
# def base_view(request):
#     user = UserProfile.objects.all()
#     portfolio =  Portfolio.objects.all()
#     contact_massage = ContactMessage.objects.all()
#     context = {
#         'user': user,
#         'portfolio': portfolio,
#         'contact_massage': contact_massage
#     }
#     return render(request, "base.html", context= context)
#
#
#
# def login_views(request):
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Xush kelibsiz, " + username + "!")
#                 return redirect("dashboard")
#             else:
#                 messages.error(request, "Login yoki parol xato!")
#     else:
#         form = UserLoginForm()
#
#     return render(request, "login.html", {"form": form})
#
#
# def logout_view(request):
#     logout(request)
#     messages.info(request, "Siz tizimdan chiqdingiz.")
#     return redirect("login")
#
# def home_view(request):
#     posts = Post.objects.all()
#     profile = None
#     if request.user.is_authenticated:
#         try:
#             profile = request.user.userprofile
#         except UserProfile.DoesNotExist:
#             profile = None
#     return render(request, "base.html", {
#         "posts": posts,
#         "profile": profile,
#     })
#
#
# @login_required(login_url='login')
# def admin(request):
#     personalinfo = PersonalInfo.objects.first()
#     skills = Skill.objects.all()
#     experiences = Experience.objects.all()
#     educations = Education.objects.all()
#     projects = Project.objects.all()
#     context = {
#         'personalinfo': personalinfo,
#         'skills': skills,
#         'experiences': experiences,
#         'educations': educations,
#         'projects': projects
#     }
#     return render(request, 'admin.html',context=context)
#
#
# @login_required(login_url='login')
# def edit_profile(request):
#     user = PersonalInfo.objects.all().first()
#     if request.method == "POST":
#         form = PersonalInfoForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect("admin")
#     else:
#         form = PersonalInfoForm(instance=user)
#
#     return render(request, "edit_profile.html", {"form": form})
#
#
# @login_required(login_url='login')
# def add_projects(request):
#     if request.method == "POST":
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin')
#     else:
#         form = ProjectForm()
#     return render(request, 'add_projects.html', {'form': form})
#
# @login_required(login_url='login')
# def message_list(request):
#     messages = ContactMessage.objects.all().order_by("-created_at")
#     return render(request, "messages.html", {"messages": messages})
#
# @login_required(login_url='login')
# def projects_list(request):
#     project = Project.objects.all()
#     return render(request,'projects.html',{'projects':project})
#
# @login_required(login_url='login')
# def delete_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.method == "POST":
#         project.delete()
#         return redirect("projects_list")
#     return render(request, "delete_confirm.html", {"project": project})
#
#
