from django.db import models

# Definition of the Civilian model
class Civilian(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Definition of the Vehicle model
class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    is_insurance_valid = models.BooleanField(default=False)
    is_registration_valid = models.BooleanField(default=False)
    owner = models.ForeignKey(Civilian, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
