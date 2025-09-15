from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile
from .forms import RegisterForm, UserProfileForm, PostForm, CommentForm
from django.http import FileResponse, Http404, HttpResponse
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from io import BytesIO
@login_required(login_url='login')
def download_cv(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Orqa fon
    p.setFillColor(HexColor("#0f1724"))
    p.rect(0, 0, width, height, fill=1)

    y = height - 50

    # Header
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(HexColor("#6EE7B7"))
    p.drawString(40, y, "Hi, I'm Adhambek")
    y -= 30

    # Kirish qismi
    p.setFont("Helvetica", 12)
    p.setFillColor(HexColor("#cfeef4"))
    p.drawString(
        40, y,
        "I build fast, accessible and delightful web applications using Django, Python and modern UI patterns."
    )
    y -= 40

    # Skills
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Skills:")
    y -= 20

    skills = ["Django", "REST API", "PostgreSQL", "HTML", "Celery"]
    for skill in skills:
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(50, y, f"- {skill}")
        y -= 15

    y -= 20
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(HexColor("#60A5FA"))
    p.drawString(40, y, "Experience:")
    y -= 20

    experiences = [
        ("2025 — Present", "Backend Developer — Acme Tech"),
        ("2024 — 2025", "Backend Developer — Freelance"),
        ("2024 — 2025", "Junior Developer — Startup"),
    ]

    for time, desc in experiences:
        p.setFont("Helvetica", 12)
        p.setFillColor(HexColor("#e6eef8"))
        p.drawString(50, y, f"{time} | {desc}")
        y -= 25

    # Tugatish
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="cv.pdf")



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # create empty profile
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("posts")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "profile.html", {"profile": request.user.profile})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "profile_edit.html", {"form": form})


# ---- Posts ----
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post_list.html", {"posts": posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by("-created_at")
    comment_form = CommentForm()
    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    })



@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts")
    else:
        form = PostForm()
    return render(request, "post_create.html", {"form": form})


@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "post_edit.html", {"form": form})


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return redirect("posts")


# ---- Comments ----
@login_required
def comment_add(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("post_detail", id=post.id)


# ---- Install ----
def install_demo(request):
    if not User.objects.filter(username="demo").exists():
        demo_user = User.objects.create_user(username="demo", password="demo123")
        UserProfile.objects.create(user=demo_user, bio="Demo blogger")

        for i in range(1, 4):
            Post.objects.create(
                title=f"Demo Post {i}",
                content="This is a demo post.",
                author=demo_user
            )
    messages.success(request, "Demo data created!")
    return redirect("posts")

def home_view(request):
    return render(request, "home.html")