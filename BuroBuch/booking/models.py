from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list

class Building(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='buildings')

    class Meta:
        unique_together = ['address', 'country',]

    def __str__(self):
        return f'{self.name} in {self.address}, {self.country}'

class Department(models.Model):
    name = models.CharField(max_length=30)
    building = models.ForeignKey(Building, blank=False, null=False, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='departments')
    coords = models.CharField(max_length=1000, null=True, blank=True, default='', validators=[validate_comma_separated_integer_list,]) # coords in the parent image

    class Meta:
        unique_together = ['name', 'building',]

    def __str__(self):
        return f'{self.building.name}: {self.name}'

class Room(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, blank=False, null=False, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='rooms')
    coords = models.CharField(max_length=1000, null=True, blank=True, default='', validators=[validate_comma_separated_integer_list,]) # coords in the parent image

    class Meta:
        unique_together = ['name', 'department',]

    def __str__(self):
        return f'{self.department.building.name}: {self.department.name}: {self.name}'

class Desk(models.Model):
    name = models.CharField(max_length=30)
    room = models.ForeignKey(Room, blank=False, null=False, on_delete=models.CASCADE)
    coords = models.CharField(max_length=1000, null=True, blank=True, default='', validators=[validate_comma_separated_integer_list,]) # coords in the parent image

    class Meta:
        unique_together = ['name', 'room',]

    def __str__(self):
        return f'{self.room.department.building.name}: {self.room.department.name}: {self.room.name}: {self.name}'

class Booking(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)

    class Meta:
        unique_together = [['desk', 'date',], ['user', 'date'],]