import datetime
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

class Init(APIView):
    """
    Populate test data
    """
    @csrf_exempt
    def get(self,request):
        for i in range(10):
            u,created=User.objects.get_or_create(username="user%d" % (i,), password="abc")
            if created:
                u.save()
            v,created=Vendor.objects.get_or_create(name='Store %d' %(i,) )
            if created:
                v.save()
            q,created=Queue.objects.get_or_create(vendor=v, name="default")
            if created:
                q.save()

        q=Queue.objects.all()[0]
        users=User.objects.all()
        for u in users:
            r=createReservation(u, q)
            r.save()
        return JSONResponse({'status':'OK'})

class Register(APIView):
    """ Register a new user.
        Input: client:  'FB' or 'G'
               client_user_id:  the user id in FB or G
               email: user email
               first_name: First name
               last_name:  Last name
               phone_number: Phone number
               access_token: the token acquired from Oauth provider
               token_expiration: date and time of token expiration

        Output json of the form {'id':<user_id>, 'status': <status>}
        The app should cache <user_id> for future REST calls
        <status> = 'new registration' for new registration
                   'access_token updated' if token has been refreshed
                   'already registered, access_token unchanged' if token hasn't been changed

        The server will check validity of the access_token
    """
    @csrf_exempt
    def put(self, request):
        print 'request', dir(request)
        return JSONResponse({'status':'testing'})
        print 'DATA', request.DATA
        profile,created = UserProfile.objects.get_or_create(client_user_id=request.DATA.client_user_id, login_client=request.DATA.client)
        # TODO: access login OAUTH provider to verify the token
        if created:
            user=User(username=request.email, email=request.email,first_name=request.first_name, last_name=request.last_name)
            user.save()
            profile.user=user
            profile.phone_number = request.phone_number
            profile.access_token = request.access_token
            profile.token_expiration = request.token_expiration
            profile.save()
            return JSONResponse({'id':user.id, 'status': 'new registration'})
        if request.access_token != profile.access_token:
            profile.access_token = request.access_token
            timeobj = datetime.datetime.strptime(request.token_expiration, "%H:%M:%S.%f").time()
            profile.token_expiration = timeobj
            profile.save()
            return JSONResponse({'id':profile.user.id, 'status': 'access_token updated'})
        return JSONResponse({'id':profile.user.id, 'status': 'already registered, access_token unchanged'})


class Enqueue(APIView):
    """ To create a new reservation for a user. This can be called from User app or Vendor app.

    """
    @csrf_exempt
    def put(self,request, user_id, queue_id):
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
    """ Mark a reservation as "served".
    """
    @csrf_exempt
    def post(self,request, queue_id, reservation_id):
        queue=Queue.objects.get(id=int(queue_id))
        today = date.today()

        reservation=Reservation.objects.get(queue=queue, reservation_number=int(reservation_id), date=today)
        if reservation.status != 'IQ':
            return JSONResponse({'status':'Already Dequeued'})

        user=reservation.user
        reservation.status = 'SV'
        reservation.save()
        return JSONResponse({'status':'OK'})


class QueryQueue(APIView):
    """ Query the status of a reservation.
    """
    @csrf_exempt
    def get(self,request, queue_id, reservation_id=None):
        today = date.today()
        queue=Queue.objects.get(id=int(queue_id))
        if reservation_id:
            reservation = Reservation.objects.get(id=int(reservation_id))
            if reservation.status!='IQ':
                return JSONResponse({"status":"Served or Cancelled"})
            res_ahead = Reservation.objects.filter(queue=queue, date=today,
                                                   reservation_number__lt=reservation.reservation_number,
                                                    status='IQ').count()
            return JSONResponse({"Your Reservation#": reservation.reservation_number,
                                 "Number of customers ahead": res_ahead,
                                 "estimate minute": max(0,res_ahead*10)})
        res_ahead = Reservation.objects.filter(queue=queue, date=today,
                                                status='IQ').count()
        return JSONResponse({"Number of customers ahead": res_ahead,
                             "estimate minute": max(0,res_ahead*10)})

