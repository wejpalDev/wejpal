from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _


class Provider(models.TextChoices):
    GOOGLE = "google", _("google")
    APPLE = "apple", _("apple")
    NOTION_AFRICA = "notion_africa", _("notion_africa")