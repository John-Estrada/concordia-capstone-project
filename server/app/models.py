from django.db import models

# Create your models here
class Controller(models.Model):
    name = models.CharField(max_length=128, unique=True)

class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null=True)
    target = models.FloatField(max_length=128)

class DataEntry(models.Model):
    data_type = models.CharField(max_length=32)
    value = models.DecimalField(decimal_places=16, max_digits=32)
    timestamp = models.DateTimeField()
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)

