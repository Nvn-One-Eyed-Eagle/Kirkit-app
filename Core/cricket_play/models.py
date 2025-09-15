from django.db import models

# Create your models here.
class player(models.Model):
    player_name = models.CharField(max_length = 30)
    player_img = models.ImageField(upload_to = "profile_pics/")
    def __str__(self):
        return self.name
