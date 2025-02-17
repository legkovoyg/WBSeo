import uuid
from django.db import models

class Prompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku_id = models.CharField(max_length=15, db_index=True)
    tone = models.CharField(max_length=50)
    language = models.CharField(max_length=25)
    exclude_keywords = models.JSONField()
    include_keywords = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sku_id', 'tone', 'language'],
                name='unique_prompt'
            )
        ]

    def __str__(self):
        return f"Prompt: {self.sku_id} - {self.tone} - {self.language} - {self.created_at}"

class GeneratedDescription(models.Model):
    prompt = models.OneToOneField(Prompt, on_delete=models.CASCADE, related_name="description")
    description = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GeneratedDescription: {self.prompt.sku_id} - {self.description} - {self.generated_at}"
