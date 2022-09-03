from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class slots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slotdate = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'slots'


class appointment(models.Model):
    PatientName = models.CharField(max_length=50)
    PatientHelathHistory = models.TextField()
    PatientPhoneNumber = models.CharField(max_length=15)
    PatientSlot = models.ForeignKey(slots, on_delete=models.CASCADE)
