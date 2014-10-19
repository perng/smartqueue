from models import *
for i in range(10):
    u=User(username="user%d" % (i,), password="abc")
    u.save()
    v=Vendor(name='Store %d' %(i,), )
    v.save()
    q=Queue(vendor=v, name="default",)
    q.save()

q=Queue.objects.get(pk=0)
users=User.objects.all()
for u in users:
    r=createReservation(u, q)
    r.save()
