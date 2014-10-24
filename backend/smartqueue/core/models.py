import json
from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

from django.forms import widgets
from rest_framework import serializers

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    phone_number = models.CharField(("phone"), max_length=13, blank=True)
    facebook_id = models.CharField(max_length=30)
    google_id = models.CharField(max_length=30)


class Vendor(models.Model):
    name = models.CharField(max_length=200)
    #phone_number = PhoneNumberField(blank=True)
    phone_number = models.CharField(("phone"), max_length=13, blank=True)
    address_1 = models.CharField(("address"), max_length=128, blank=True)
    address_2 = models.CharField(("address cont'd"), max_length=128, blank=True)

    city = models.CharField(("city"), max_length=64,  blank=True)
    state = models.CharField(("state"),max_length=2,  default="CA")
    zip_code = models.CharField(("zipcode"), max_length=5, blank=True)
    def __str__(self):
        return self.name


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        #fields = ('name', 'phone_number', )

class Queue(models.Model):
    name = models.CharField(max_length=200, blank=True)
    vendor = models.ForeignKey(Vendor)
    group_size = models.IntegerField(null=True)

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('name', 'vendor', 'group_size' )


STATUS_CHOICES = (
    ("IQ", "In Queue"),
    ("SV", "Served"),
    ("CC", "Cancelled"),
)
class Reservation(models.Model):
    user = models.ForeignKey(User)
    queue = models.ForeignKey(Queue)
    reservation_number = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)

def createReservation(user, queue):
    r=Reservation(user=user, queue=queue, status='IQ')
    n=len(Reservation.objects.filter(queue=queue, date=r.date).exclude(status="IQ"))
    r.reservation_number = n+1
    r.save()
    return r

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('user', 'queue', 'reservation_number', 'date', 'time', 'status')


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=20)
