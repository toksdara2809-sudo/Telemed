from django.contrib import admin
from .models import Consultation, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'message', 'timestamp')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [ChatMessageInline]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'sender', 'message', 'timestamp')
    list_filter = ('timestamp',)
