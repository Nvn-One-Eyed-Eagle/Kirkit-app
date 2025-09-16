from django.shortcuts import render, redirect
from .models import player

def home(request):
    errors = []
    if request.method == "POST":
        name = request.POST.get("player_name")
        img  = request.FILES.get("player_img")

        # Validation
        if not name:
            errors.append("Name is required")
        if not img:
            errors.append("Image is required")
        elif not img.content_type.startswith("image/"):
            errors.append("File must be an image")

        # Only save if no errors
        if not errors:
            player.objects.create(player_name=name, player_img=img)
            return redirect("home")

    profile = player.objects.all()
    return render(request, "home.html", {"profile": profile, "errors": errors})
