from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#specifying-a-custom-user-model
# different approach
class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=50, default='TOURIST', blank=False)

    pass


class TouristUser(BaseUser):

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.user_type = 'TOURIST'
        return super(TouristUser, self).save()


class AgencyUser(BaseUser):
    arrangement_place = models.CharField(max_length=50, blank=False, null=False)
    phone = PhoneNumberField(max_length=50, null=False, blank=False, unique=True)
    agency_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.email
        self.user_type = 'AGENCY'
        return super(AgencyUser, self).save()


class Arrangement(models.Model):
    place = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    tourists = models.ManyToManyField(TouristUser, related_name='tourists')
    agency = models.ForeignKey(AgencyUser, on_delete=models.CASCADE, null=False)
    arrangement_start_time = models.DateField(null=False, blank=False)
    arrangement_end_time = models.DateField(null=False, blank=False)
    price_per_person = models.FloatField(null=False, blank=False,
                                         validators=[MinValueValidator(0.0)])
    image = models.ImageField(upload_to='images/')
    date_created = models.DateTimeField(auto_now_add=True)
    number_of_free_seats = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        ordering = ['arrangement_start_time']

    def __str__(self):
        return str(self.place)

    # month = models.CharField(max_length=25, default="")

    # def save(self):
    #     return super(Arrangement, self).save()
