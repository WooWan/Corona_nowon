from django.contrib import admin
from .models import Corona
# Register your models here.
@admin.register(Corona)
class CoronaAdmin(admin.ModelAdmin):
	list_display=['region']