from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import Profile, Project, CaseStudy, BlogPost, Testimonial, ResumeItem, ContactMessage
from .forms import ContactForm, ProjectForm, ProfileForm


# ------------------- Base / Home -------------------
def index(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    else:
        profile = Profile.objects.first()  # Agar foydalanuvchi login qilmagan bo'lsa

    context = {
        'user': profile,
        'portfolio': Project.objects.filter(profile=profile) if profile else [],
        'case_studies': CaseStudy.objects.filter(profile=profile) if profile else [],
        'blog_posts': BlogPost.objects.filter(profile=profile) if profile else [],
        'testimonials': Testimonial.objects.filter(profile=profile) if profile else [],
        'resume_items': ResumeItem.objects.filter(profile=profile) if profile else [],
        'contact_form': ContactForm(),
    }

    # Contact form POST
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


# ------------------- Login / Logout -------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {username}!")
                return redirect("admin_panel")
            else:
                messages.error(request, "Login yoki parol xato!")
        else:
            messages.error(request, "Noto'g'ri ma'lumotlar kiritildi.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect("base")


# ------------------- PDF CV Download -------------------
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    styles = getSampleStyleSheet()

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

    # Faqat bitta asosiy profilni olish (masalan, birinchi profil)
    profile = Profile.objects.first()

    # Header
    if profile:
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(HexColor("#6EE7B7"))
        p.drawString(40, y, f"Salom, men {profile.user.first_name or profile.user.username} — {profile.role}")
        y -= 30

        # Lead text (bio)
        if profile.bio:
            y = new_page_if_needed(y)
            style = styles["Normal"]
            style.fontName = "Helvetica"
            style.fontSize = 12
            style.textColor = HexColor("#cfeef4")
            p_obj = Paragraph(profile.bio, style)
            w, h = p_obj.wrap(width - 80, y)
            p_obj.drawOn(p, 40, y - h)
            y -= h + 20

    # Resume (tajriba va ta’lim)
    resume_items = ResumeItem.objects.filter(profile=profile)
    if resume_items.exists():
        y = new_page_if_needed(y)
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Rezyume:")
        y -= 20
        for item in resume_items:
            y = new_page_if_needed(y)
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(HexColor("#f9fafb"))
            p.drawString(50, y, f"{item.title} ({item.duration})")
            y -= 15
            style.fontSize = 11
            p_obj = Paragraph(item.description, style)
            w, h = p_obj.wrap(width - 100, y)
            p_obj.drawOn(p, 60, y - h)
            y -= h + 15

    # Projects (DB’dan)
    projects = Project.objects.filter(profile=profile)
    if projects.exists():
        y = new_page_if_needed(y)
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#60A5FA"))
        p.drawString(40, y, "Loyihalar:")
        y -= 20
        for proj in projects:
            y = new_page_if_needed(y)
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(HexColor("#f9fafb"))
            p.drawString(50, y, f"{proj.name}:")
            y -= 15
            style.fontSize = 11
            p_obj = Paragraph(proj.description, style)
            w, h = p_obj.wrap(width - 100, y)
            p_obj.drawOn(p, 60, y - h)
            y -= h + 15

    # Case Studies (DB’dan)
    case_studies = CaseStudy.objects.filter(profile=profile)
    if case_studies.exists():
        y = new_page_if_needed(y)
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(HexColor("#f9fafb"))
        p.drawString(40, y, "Case Studies:")
        y -= 20
        for case in case_studies:
            y = new_page_if_needed(y)
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(HexColor("#f9fafb"))
            p.drawString(50, y, case.title)
            y -= 15
            style.fontSize = 11
            p_obj = Paragraph(case.description, style)
            w, h = p_obj.wrap(width - 100, y)
            p_obj.drawOn(p, 60, y - h)
            y -= h + 15

    # Tugatish
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")


# ------------------- Admin Panel -------------------
@login_required
def admin_panel(request):
    return render(request, 'admin_panel.html')


# ------------------- Projects CRUD -------------------
@login_required
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})


@login_required(login_url='login')
def add_projects(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = request.user.profile  # yoki kerakli profile obyekt
            project.save()
            return redirect('admin_panel')
    else:
        form = ProjectForm()
    return render(request, 'add_projects.html', {'form': form})



@login_required
def update_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Loyiha muvaffaqiyatli tahrirlandi ✅")
            return redirect('projects_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form})


@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    messages.success(request, "Loyiha muvaffaqiyatli o‘chirildi ✅")
    return redirect('projects_list')


# ------------------- Messages -------------------
@login_required
def message_list(request):
    messages_list = ContactMessage.objects.all()
    return render(request, 'message_list.html', {'messages': messages_list})


# ------------------- Edit Profile -------------------
@login_required(login_url='login')
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('admin_panel')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
