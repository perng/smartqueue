from django.test import TestCase

# Create your tests here.

from models import *


class QueueTest(TestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(username='perng')
        if created:
            self.user.email='charles@perng.com'
            self.user.password = 'pbkdf2_sha256$12000$aWxQu6mHHaDA$pfqaju6fGCuSO/S07mharMwP0sAKLD8pVIvGBS/nprU='
            self.user.save()
        vendors = Vendor.objects.all()
        if len(vendors)==0:
            self.vendor=Vendor(name="Barefoot Cafe", phone_number="405-555-555")
            self.vendor.save()
        else:
            self.vendor = vendors[0]
    def test_enqueue(self):
        pass
