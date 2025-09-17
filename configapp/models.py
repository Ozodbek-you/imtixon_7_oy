from django.db import models
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


# Bu model standart Django User modelini kengaytirib, qo'shimcha profil ma'lumotlarini saqlaydi.
# Har bir foydalanuvchiga bitta profil bog'langan bo'ladi.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=100, default="Backend Dasturchi")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, default="O‘zbekiston")
    is_freelance_available = models.BooleanField(default=True)
    email = models.EmailField(blank=True, null=True)

    # HTMLda "1 Year Experience" kabi matnlar bo'lgani uchun CharField ishlatamiz.
    experience = models.CharField(max_length=50, default="1 Yil Tajriba")
    projects_count = models.CharField(max_length=50, default="10 dan ortiq loyiha")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"{self.user.username} profili"


# Bu model portfoliodagi har bir loyihani ifodalaydi.
# ForeignKey orqali loyihalarni ma'lum bir profilga bog'laydi.
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.CharField(max_length=255,
                              help_text="Loyiha uchun ishlatilgan ko'nikmalar (vergul bilan ajratilgan).")
    thumbnail = models.ImageField(upload_to='project_thumbnails/', blank=True, null=True)

    class Meta:
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self):
        return self.name


# Bu model "Case Studies" bo'limidagi case study'larni ifodalaydi.
class CaseStudy(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='case_studies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    results = models.TextField(help_text="Natijalarni har birini yangi qatordan kiriting.")
    technologies = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"

    def __str__(self):
        return self.title


# Bu model blog postlari yoki maqolalar uchun.
class BlogPost(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255)
    summary = models.TextField(help_text="Maqolaning qisqacha mazmuni.")
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', blank=True, null=True)
    full_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Postlar"

    def __str__(self):
        return self.title


# Bu model mijozlar fikr-mulohazalarini saqlaydi.
class Testimonial(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='testimonials')
    text = models.TextField()
    author = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Fikr-mulohaza"
        verbose_name_plural = "Fikr-mulohazalar"

    def __str__(self):
        return f"{self.author} tomonidan yozilgan fikr-mulohaza"


# Bu model rezyume (resume) bo'limidagi ma'lumotlarni saqlaydi.
class ResumeItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='resume_items')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=20, default="tajriba")

    class Meta:
        verbose_name = "Rezyume elementi"
        verbose_name_plural = "Rezyume elementlari"

    def __str__(self):
        return self.title


# Bu model aloqa (contact) formasidan yuborilgan xabarlarni saqlaydi.
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aloqa xabari"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} dan xabar"