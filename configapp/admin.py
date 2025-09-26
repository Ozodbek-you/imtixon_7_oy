from django.contrib import admin
from .models import *
# from .models import Portfolio

# @admin.register(Portfolio)
# class PortfolioAdmin(admin.ModelAdmin):
#     list_display = ("name", "role")

# admin.site.register(UserProfile)
admin.site.register([ContactMessage, ResumeItem, Testimonial,BlogPost,CaseStudy,Project,Profile])

