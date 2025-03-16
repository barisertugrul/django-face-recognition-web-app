from django.db import models
import os  # Görüntü adını ve uzantısını ayırmak için kullanılır

class FaceRecognition(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/')
    record_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, editable=False)  # Yeni name alanı

    def save(self, *args, **kwargs):
        # Modelin kaydedilmesini sağlayalım ki record_date değeri otomatik olarak ayarlansın
        super(FaceRecognition, self).save(*args, **kwargs)

        # Orijinal görüntü adını uzantısız olarak al
        if self.record_date and self.image:
            original_filename = os.path.splitext(os.path.basename(self.image.name))[0]  # Uzantıyı kaldırdık
            self.name = f"{original_filename}_{self.record_date.strftime('%Y-%m-%d_%H-%M-%S')}"
            # Değişikliği kaydet
            super(FaceRecognition, self).save(update_fields=['name'])

    def __str__(self):
        return self.name
