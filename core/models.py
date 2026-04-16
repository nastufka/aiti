from django.db import models
from datetimeutc.fields import DateTimeUTCField
from simple_history.models import HistoricalRecords

class TimeStampedModel(models.Model):
    created_at = DateTimeUTCField(auto_now_add=True)
    updated_at = DateTimeUTCField(auto_now=True)

    class Meta:
        abstract = True

class BaseModel(TimeStampedModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True