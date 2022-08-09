from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Arrangement, TouristUser, AgencyUser


class ArrangementForm(ModelForm):
    class Meta:
        model = Arrangement
        fields = ['place',
                  'description',
                  'arrangement_start_time',
                  'arrangement_end_time',
                  'price_per_person',
                  'image',
                  'number_of_free_seats'
                  ]


class TouristUserCreationForm(UserCreationForm):
    class Meta:
        model = TouristUser
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email']


class AgencyUserCreationForm(UserCreationForm):
    class Meta:
        model = AgencyUser
        fields = ['arrangement_place',
                  'phone',
                  'email',
                  'agency_name',
                  'first_name',
                  'last_name']


class TouristUserEditForm(TouristUserCreationForm):
    class Meta:
        model = TouristUser
        fields = ['first_name',
                  'last_name',
                  'email']


class AgencyUserEditForm(AgencyUserCreationForm):

    class Meta:
        model = AgencyUser
        fields = ['arrangement_place',
                  'phone',
                  'agency_name',
                  'first_name',
                  'last_name']
