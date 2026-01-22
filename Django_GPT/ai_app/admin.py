from django.contrib import admin
from .models import ChatHistory

# Register your models here.
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'model_type', 'created_at']
    list_filter = ['model_type', 'created_at']
    search_fields = ['user__username', 'input_text']