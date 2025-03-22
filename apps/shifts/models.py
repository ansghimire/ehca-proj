from django.db import models


class Nurse(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Availability(models.Model):
    days = models.CharField(max_length=255, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
    date = models.DateField()
    note = models.FileField(upload_to='notes/', null=True, blank=True)

    def __str__(self):
        return f'{self.days} - {self.date}'




class Shift(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    shift_type = models.CharField(max_length=255, choices=[('AM', 'AM'), ('PM', 'PM')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f'{self.nurse.name} - {self.shift_type}'


    