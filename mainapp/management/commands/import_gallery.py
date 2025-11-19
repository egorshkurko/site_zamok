
from django.core.management.base import BaseCommand
from sitecore.models import GalleryImage
from pathlib import Path

class Command(BaseCommand):
    help="Import gallery images from media/gallery"

    def handle(self, *args, **kwargs):
        folder=Path("media/gallery")
        count=0
        for f in folder.glob("*"):
            if f.is_file():
                GalleryImage.objects.create(image=f"gallery/{f.name}")
                count+=1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} images"))
