from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login_table(AbstractUser):
    usertype=models.CharField(max_length=25)

class User_registration(models.Model):

    name=models.CharField(max_length=25,null=True)
    usertype=models.CharField(max_length=25,null=True)
    address=models.CharField(max_length=150,null=True)
    contact=models.CharField(max_length=25,null=True)
    email=models.EmailField(null=True)
    profile_picture=models.ImageField(null=True)
    id_card=models.FileField(null=True)
    login_id=models.ForeignKey(Login_table,on_delete=models.CASCADE,null=True)

class Staff_registration(models.Model):

    name=models.CharField(max_length=25,null=True)
    contact=models.CharField(max_length=25,null=True)
    email=models.EmailField(null=True)
    profile_picture=models.ImageField(null=True)
    login_id=models.ForeignKey(Login_table,on_delete=models.CASCADE,null=True)


class Add_food(models.Model):

    name=models.CharField(max_length=25,null=True)
    quantity=models.CharField(max_length=25,null=True)
    category=models.CharField(max_length=25,null=True)
    price=models.CharField(max_length=25,null=True)
    description=models.CharField(max_length=250,null=True)
    food_image=models.ImageField(null=True)
    rating=models.CharField(max_length=25,null=True)
    posted_date=models.CharField(max_length=25,null=True)
    staff_id=models.ForeignKey(Staff_registration,on_delete=models.CASCADE,null=True)


class User_booking_food(models.Model):

    user_id=models.ForeignKey(User_registration,on_delete=models.CASCADE,null=True)
    food_id=models.ForeignKey(Add_food,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,null=True)
    quantity=models.IntegerField(null=True)
    pick_up_time=models.TimeField(null=True)
    price=models.IntegerField(null=True)
    contact=models.IntegerField(null=True)
    payment_status=models.BooleanField(default=False)
    cancel_status=models.BooleanField(default=False)
    booked_on=models.DateTimeField(null=True)


class Add_table(models.Model):

    table_no=models.CharField(max_length=25,null=True)
    time_from=models.TimeField(null=True)
    time_to=models.TimeField(null=True)
    booking_status=models.BooleanField(default=False)
    booked_on=models.DateTimeField(null=True)
    added_on=models.DateField(null=True)
    staff_id=models.ForeignKey(Staff_registration,on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(User_registration,on_delete=models.CASCADE,null=True)



class User_feedbacks(models.Model):

    user_id=models.ForeignKey(User_registration,on_delete=models.CASCADE,null=True)
    booking_id=models.ForeignKey(User_booking_food,on_delete=models.CASCADE,null=True)
    feedback=models.CharField(max_length=250,null=True)
    rating=models.IntegerField(null=True)
    date=models.DateTimeField(null=True)

