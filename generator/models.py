from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

class PasswordEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    generated_password = models.CharField(max_length=128)

    class Meta:
        db_table = 'password_entry'

    def __str__(self):
        return f"{self.service_name} - {self.user.username}"

