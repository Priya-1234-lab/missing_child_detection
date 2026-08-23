
from django.db import models
from accounts.models import Parent

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    photo = models.ImageField(upload_to="child_photos/")
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
