import subprocess
from pathlib import Path

import imageio_ffmpeg
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps

from hotel.models import GalleryImage, HeroSlide, NearbyAttraction, Room, RoomGalleryImage, ShowcaseSection


class Command(BaseCommand):
    help = "Convert uploaded hotel images/videos into optimized WebP/MP4 assets and wire them into the site."

    def add_arguments(self, parser):
        parser.add_argument("--skip-video", action="store_true", help="Only optimize images and database image fields.")
        parser.add_argument("--force", action="store_true", help="Regenerate existing optimized assets.")
        parser.add_argument("--delete-originals", action="store_true", help="Delete source TIF/MP4 files after optimized assets are created.")

    def handle(self, *args, **options):
        media_seed = settings.MEDIA_ROOT / "seed"
        media_out = settings.MEDIA_ROOT / "optimized"
        video_out = settings.BASE_DIR / "static" / "videos"
        media_out.mkdir(parents=True, exist_ok=True)
        video_out.mkdir(parents=True, exist_ok=True)

        optimized_images = self.optimize_images(media_seed, media_out, force=options["force"], delete_originals=options["delete_originals"])
        if optimized_images:
            self.update_database_images(optimized_images)

        if not options["skip_video"]:
            self.optimize_videos(media_seed, video_out, force=options["force"], delete_originals=options["delete_originals"])

        self.stdout.write(self.style.SUCCESS("Hotel media optimized."))

    def optimize_images(self, source_dir, output_dir, force=False, delete_originals=False):
        files = sorted(source_dir.glob("*.TIF")) + sorted(source_dir.glob("*.tif"))
        optimized = []
        for source in files:
            target = output_dir / f"{source.stem.lower()}.webp"
            if target.exists() and not force:
                optimized.append(f"optimized/{target.name}")
                continue

            image = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
            image.thumbnail((2200, 2200), Image.Resampling.LANCZOS)
            image.save(target, "WEBP", quality=84, method=6)
            optimized.append(f"optimized/{target.name}")
            self.stdout.write(f"image: {source.name} -> {target.name} ({target.stat().st_size // 1024} KB)")
            if delete_originals and target.exists():
                source.unlink()
                self.stdout.write(f"deleted source image: {source.name}")
        return optimized

    def update_database_images(self, images):
        if not images:
            return

        hero = HeroSlide.objects.order_by("ordering", "id").first()
        if hero:
            hero.image = images[0]
            hero.save(update_fields=["image"])

        rooms = list(Room.objects.filter(active=True).order_by("ordering", "id"))
        for room, image in zip(rooms, images[1:5]):
            room.main_image = image
            room.save(update_fields=["main_image"])

        gallery_images = list(GalleryImage.objects.order_by("ordering", "id"))
        for item, image in zip(gallery_images, images):
            item.image = image
            item.save(update_fields=["image"])

        room_gallery = list(RoomGalleryImage.objects.order_by("room__ordering", "ordering", "id"))
        for item, image in zip(room_gallery, images[5:] + images):
            item.image = image
            item.save(update_fields=["image"])

        attractions = list(NearbyAttraction.objects.order_by("ordering", "id"))
        for item, image in zip(attractions, images[8:] + images):
            item.image = image
            item.save(update_fields=["image"])

        showcase = ShowcaseSection.objects.first()
        if showcase and len(images) > 10:
            showcase.image = images[10]
            showcase.save(update_fields=["image"])

    def optimize_videos(self, source_dir, output_dir, force=False, delete_originals=False):
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        jobs = [
            {
                "source": source_dir / "HOTEL.mp4",
                "target": output_dir / "hotel-hero.mp4",
                "poster": output_dir / "hotel-hero-poster.webp",
                "start": "00:00:08",
                "duration": "14",
                "vf": "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720",
                "crf": "30",
            },
            {
                "source": source_dir / "HOTEL 01.mp4",
                "target": output_dir / "hotel-lobby.mp4",
                "poster": output_dir / "hotel-lobby-poster.webp",
                "start": "00:00:04",
                "duration": "28",
                "vf": "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
                "crf": "31",
            },
            {
                "source": source_dir / "HOTEL 02.mp4",
                "target": output_dir / "hotel-rooms.mp4",
                "poster": output_dir / "hotel-rooms-poster.webp",
                "start": "00:00:05",
                "duration": "28",
                "vf": "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
                "crf": "31",
            },
            {
                "source": source_dir / "HOTEL.mp4",
                "target": output_dir / "hotel-heritage.mp4",
                "poster": output_dir / "hotel-heritage-poster.webp",
                "start": "00:00:45",
                "duration": "28",
                "vf": "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
                "crf": "31",
            },
        ]

        for job in jobs:
            if not job["source"].exists():
                self.stdout.write(self.style.WARNING(f"missing video: {job['source'].name}"))
                continue
            if job["target"].exists() and job["poster"].exists() and not force:
                continue

            cmd = [
                ffmpeg,
                "-y",
                "-ss",
                job["start"],
                "-i",
                str(job["source"]),
                "-t",
                job["duration"],
                "-an",
                "-vf",
                job["vf"],
                "-r",
                "24",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                job["crf"],
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(job["target"]),
            ]
            self.stdout.write(f"video: {job['source'].name} -> {job['target'].name}")
            subprocess.run(cmd, check=True)

            poster_cmd = [
                ffmpeg,
                "-y",
                "-ss",
                "00:00:01",
                "-i",
                str(job["target"]),
                "-frames:v",
                "1",
                "-vf",
                "scale=900:-2",
                str(job["poster"]),
            ]
            subprocess.run(poster_cmd, check=True)
            self.stdout.write(f"video size: {job['target'].stat().st_size // 1024} KB")

        if delete_originals:
            for source in {job["source"] for job in jobs if job["source"].exists()}:
                source.unlink()
                self.stdout.write(f"deleted source video: {source.name}")
