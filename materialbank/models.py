from django.db import models
import os

class Material(models.Model):
    CATEGORY_CHOICES = [
        ('fabric', 'Fabric'),
        ('accessory', 'Accessory'),
        ('tool', 'Tool'),
        ('decor', 'Decor'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    donator_name = models.CharField(max_length=100, blank=True, null=True)
    current_with = models.CharField(max_length=100, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class DonationRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='donation_requests/', blank=True, null=True)
    donator_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    collected_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    def save(self, *args, **kwargs):
        old = DonationRequest.objects.filter(pk=self.pk).first() if self.pk else None
        super().save(*args, **kwargs)

        # If status changed and now is rejected → delete old image
        if old and old.status != self.status and self.status == "Rejected":
            if old.image and os.path.isfile(old.image.path):
                os.remove(old.image.path)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Points(models.Model):
    email = models.EmailField(unique=True)
    total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.email} - {self.total_points} points"
