from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=50)  # 'summarize', 'sentiment', 'generate'
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.model_type} - {self.created_at}"