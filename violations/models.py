from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class Violations(models.Model):
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    fine_min = models.IntegerField()
    fine_max = models.IntegerField()
    punishment = models.TextField()
    age_group = models.CharField(max_length=10, choices=[('adult', '成人'), ('minor', '未成年')])  # 年齢区分を追加

    def __str__(self):
        return self.name

class ViolationSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Violation = models.ForeignKey(Violations, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    total_fine_min = models.IntegerField()
    total_fine_max = models.IntegerField()
    possible_punishment = models.TextField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    