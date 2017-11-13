from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	pass

@admin.register(Reader)
class BookAdmin(admin.ModelAdmin):
	pass

@admin.register(Category)
class BookAdmin(admin.ModelAdmin):
	pass

@admin.register(Location)
class BookAdmin(admin.ModelAdmin):
	pass