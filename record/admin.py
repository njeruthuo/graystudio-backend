from django.contrib import admin
from .models import Record, Client


class RecordInline(admin.TabularInline):
    model = Record
    extra = 1

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['client__name','amount_paid', 'date']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'date_joined', 'total_points']
    inlines = [RecordInline]
