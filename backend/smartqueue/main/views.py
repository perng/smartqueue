from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class Enqueue(APIView):
    @csrf_exempt
    def get(self,request, user_id, queue_id):
        user=User.objects.get(id=int(user_id))
        queue=Queue.objects.get(id=int(queue_id))
        today = date.today()

        # if the user is already in queue and still waiting, get the reservation
        reservations = Reservation.objects.filter(user=user, queue=queue, date=today, status='IQ')
        if len(reservations)>0:
            reservation = reservations[0]
        else:
            rsn=Reservation.objects.filter(queue=queue,date=today)
            if len(rsn)==0:
                rn= 1
            else:
                rn=rsn.latest('reservation_number').reservation_number+1
            reservation = Reservation(user=user, queue=queue, status='IQ', reservation_number=rn)
            reservation.save()
        serializer = ReservationSerializer(reservation)
        return JSONResponse(serializer.data)

class Dequeue(APIView):
    @csrf_exempt
    def get(self,request, queue_id, reservation_id):
        queue=Queue.objects.get(id=int(queue_id))
        today = date.today()
        reservation=Reservation.objects.get(queue=queue, reservation_number=int(reservation_id), date=today)
        if reservation.status != 'IQ':
            return JSONResponse({'status':'Already Dequeued'})

        user=reservation.user
        reservation.status = 'SV'
        reservation.save()
        return JSONResponse({'status':'OK'})
