from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    country_code = models.CharField(max_length=5)
    password = models.CharField(max_length=100)
    pradesh = models.CharField(max_length=50)
    reference_sant = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.mobile}"

class EventDetail(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='event_details', null=True)
    sabha_name = models.CharField(max_length=255)
    sabha_date = models.DateField()

    def __str__(self):
        return f"{self.sabha_name} ({self.sabha_date})"

class Pradesh(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Sant(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SabhaOption(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

from django.db import models

class DashboardContent(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    raw_drive_folder_url = models.URLField(null=True, blank=True)
    raw_zip_download_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title or "Dashboard Content"

    @property
    def grid_view_url(self):
        """
        Convert the folder URL into an embedded grid view.
        """
        if self.raw_drive_folder_url and "/folders/" in self.raw_drive_folder_url:
            folder_id = self.raw_drive_folder_url.split("/folders/")[1].split("?")[0]
            return f"https://drive.google.com/embeddedfolderview?id={folder_id}#grid"
        return None

    @property
    def direct_zip_download_url(self):
        """
        Convert the file URL into a direct download link.
        """
        if self.raw_zip_download_url:
            if "/file/d/" in self.raw_zip_download_url:
                file_id = self.raw_zip_download_url.split("/file/d/")[1].split("/")[0]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            elif "id=" in self.raw_zip_download_url:
                file_id = self.raw_zip_download_url.split("id=")[1].split("&")[0]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
        return None



