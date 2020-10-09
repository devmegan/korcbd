from django.db import models


# Create your models here.

class AboutSection(models.Model):
    section_title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=False)

    # see section title in admin
    def __str__(self):
        return self.section_title
