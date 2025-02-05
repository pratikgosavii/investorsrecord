from django.db import models


from users.models import User
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')



from users.models import User




class operator(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=120, unique=False)
    mobile_no = models.IntegerField()
    remark = models.CharField(max_length=120, unique=False)
    is_active = models.BooleanField(default = True)

    
    def __str__(self):
        return self.name

class investor(models.Model):

    name = models.CharField(max_length=120, unique=False)
    address = models.CharField(max_length=120, unique=False)
    mobile_no = models.IntegerField()
    remark = models.CharField(max_length=120, unique=False)
    is_active = models.BooleanField(default = True)
    
    
    def __str__(self):
        return self.name

class transactions(models.Model):

    operator = models.ForeignKey(operator, on_delete=models.CASCADE)
    investor = models.ForeignKey(investor, on_delete=models.CASCADE)
    amount = models.IntegerField()
    remark = models.CharField(max_length=120, unique=False, blank=False, null = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.operator.name

