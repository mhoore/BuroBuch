from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.

class Map(models.Model):
    name = models.CharField(max_length=30, unique=True)
    shape = models.CharField(max_length=20, null=True, blank=True, default='rect')
    coords = models.CharField(max_length=40, null=True, blank=True, default='0,0,0,0', validators=[validate_comma_separated_integer_list,])

    def __str__(self):
        return f'{self.name}'

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
    map = models.ForeignKey(Map, blank=True, null=True, on_delete=models.SET_NULL) # map to parent image

    class Meta:
        unique_together = ['name', 'building',]

    def __str__(self):
        return f'{self.name}'

class Room(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department, blank=False, null=False, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, default=None, upload_to='rooms')
    map = models.ForeignKey(Map, blank=True, null=True, on_delete=models.SET_NULL) # map to parent image

    class Meta:
        unique_together = ['name', 'department',]

    def __str__(self):
        return f'{self.name}'

class Desk(models.Model):
    name = models.CharField(max_length=30)
    room = models.ForeignKey(Room, blank=False, null=False, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, blank=True, null=True, on_delete=models.SET_NULL) # map to parent image

    class Meta:
        unique_together = ['name', 'room',]

    def __str__(self):
        return f'{self.name}'

class Booking(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)

    class Meta:
        unique_together = [['desk', 'date',], ['user', 'date'],]