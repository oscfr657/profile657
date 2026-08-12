from django.test import TestCase
from django.utils import timezone
from django.contrib.sites.models import Site
from datetime import timedelta

from profile657.models import Lock


class LockModelTests(TestCase):
    def setUp(self):
        self.site = Site.objects.create(domain="localhost", name="Test Site")
        self.now = timezone.now()

    def test_create_lock_basic(self):
        """Tests that a Lock can be created with only the required fields."""
        lock = Lock.objects.create(startdate=self.now)
        self.assertEqual(Lock.objects.count(), 1)
        self.assertEqual(lock.startdate, self.now)
        self.assertIsNone(lock.enddate)
        self.assertIsNone(lock.site)

    def test_save_method_slugifies_password(self):
        """Tests that the password is slugified when the model is saved."""
        lock = Lock.objects.create(
            startdate=self.now,
            password="My Secret Password! 123"
        )
        self.assertEqual(lock.password, "my-secret-password-123")

    def test_save_method_with_none_password(self):
        """
        Tests that an empty password remains None and is not 
        incorrectly slugified to the string 'none'.
        """
        lock = Lock.objects.create(startdate=self.now, password=None)
        self.assertIsNone(lock.password)

    def test_str_representation_with_enddate(self):
        """Tests the __str__ method when enddate is set."""
        end_time = self.now + timedelta(days=5)
        lock = Lock.objects.create(startdate=self.now, enddate=end_time)
        
        expected_start = self.now.strftime('%Y-%m-%d %H:%M')
        expected_end = end_time.strftime('%Y-%m-%d %H:%M')
        expected_str = f"Lock ({expected_start} to {expected_end})"
        
        self.assertEqual(str(lock), expected_str)

    def test_str_representation_without_enddate(self):
        """Tests the __str__ method when enddate is missing (null)."""
        lock = Lock.objects.create(startdate=self.now)
        
        expected_start = self.now.strftime('%Y-%m-%d %H:%M')
        expected_str = f"Lock ({expected_start} to indefinitely)"
        
        self.assertEqual(str(lock), expected_str)

    def test_site_relationship_has_no_related_name(self):
        """
        Tests the ForeignKey relationship to Site works, but ensures
        there is no reverse relation created due to related_name='+'.
        """
        lock = Lock.objects.create(startdate=self.now, site=self.site)
        
        # The forward relation works fine
        self.assertEqual(lock.site, self.site)
        
        # Verify that reverse relation 'Locks' or 'lock_set' does not exist
        with self.assertRaises(AttributeError):
            _ = self.site.Locks.all()
            
        with self.assertRaises(AttributeError):
            _ = self.site.lock_set.all()
