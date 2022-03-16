from django.db import models

# Create your models here
class Controller(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'name: {self.name}'

class Target(models.Model):
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null = True)
    type = models.CharField(max_length=128, null = False)
    value = models.FloatField(max_length=128, null = False)

class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null=True)
    target = models.FloatField(max_length=128)

    def __str__(self):
        return f'name: {self.name}, controller: {self.controller.name}, target: {self.target}'

class DataEntry(models.Model):
    data_type = models.CharField(max_length=32)
    value = models.DecimalField(decimal_places=16, max_digits=32)
    timestamp = models.DateTimeField()
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'data_type: {self.data_type}, value: {self.value}, timestamp: {self.timestamp}, controller: {self.controller}, device: {self.device}'

