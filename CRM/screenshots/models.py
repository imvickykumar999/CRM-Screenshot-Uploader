from django.db import models

class Screenshot(models.Model):
    file = models.ImageField(upload_to='screenshots/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Screenshot {self.id} uploaded at {self.uploaded_at}"
