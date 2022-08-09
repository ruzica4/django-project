from datetime import timedelta, date

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Arrangement, BaseUser, AgencyUser, TouristUser
from .forms import ArrangementForm, TouristUserCreationForm, AgencyUserCreationForm, TouristUserEditForm, \
    AgencyUserEditForm

from .decorators import user_is_agency, user_is_tourist


# Create your views here.
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            username = BaseUser.objects.get(username=username)
        except:
            messages.error(request, 'User doesn\'t exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    page = 'register_user'

    form = TouristUserCreationForm()
    if request.method == 'POST':
        form = TouristUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There was an issue during the registration process.')

    return render(request, 'base/login_registration.html', {'form': form})


def register_agency(request):
    page = 'register_agency'

    form = AgencyUserCreationForm()
    if request.method == 'POST':
        form = AgencyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There was an issue during the registration process.')

    return render(request, 'base/login_registration.html', {'form': form})


def home(request):
    startdate = date.today()
    plus_5_days = startdate + timedelta(days=5)

    if request.user.is_authenticated and request.user.user_type == 'TOURIST':
        arrangements_5_days = Arrangement.objects.filter(Q(arrangement_start_time__gte=plus_5_days))
        arrangements = Arrangement.objects.all()
        user = TouristUser.objects.get(id=request.user.id)
        my_past_arrangements = Arrangement.objects.filter(tourists__in=[user])

    elif request.user.is_authenticated and request.user.user_type == 'AGENCY':
        arrangements_5_days = Arrangement.objects.filter(
            Q(arrangement_start_time__gte=plus_5_days) & Q(agency=request.user.id))
        arrangements = Arrangement.objects.filter(agency=request.user.id)
        my_past_arrangements = []
    else:
        arrangements_5_days = Arrangement.objects.filter(Q(arrangement_start_time__gte=plus_5_days))
        arrangements = Arrangement.objects.all()
        my_past_arrangements = []
    context = {'arrangements': arrangements, 'arrangements_5_days': arrangements_5_days,
               'my_past_arrangements': my_past_arrangements}
    return render(request, 'base/home.html', context)


def arrangement(request, pk):
    try:
        arrangement = Arrangement.objects.get(id=pk)
    except Arrangement.DoesNotExist:
        raise Http404("Given arrangement does not exist!")

    startdate = date.today()
    plus_5_days = startdate + timedelta(days=5)
    if arrangement in Arrangement.objects.filter(
            Q(arrangement_start_time__gte=plus_5_days) & Q(
                number_of_free_seats__gte=1)) and request.user.is_authenticated and request.user.user_type == 'TOURIST':
        res = True
    else:
        res = False
    arrangement_tourists = arrangement.tourists.all()
    context = {'arrangement': arrangement, 'res': res, 'arrangement_tourists': arrangement_tourists}
    return render(request, 'base/arrangement.html', context)


@login_required(login_url='login')
@user_is_agency
def create_arrangement(request):
    form = ArrangementForm()

    if request.method == 'POST':
        form = ArrangementForm(request.POST, request.FILES)

        if form.is_valid():
            start_date = form['arrangement_start_time'].value()
            end_date = form['arrangement_end_time'].value()
            if start_date > end_date:
                print('her')
                messages.error(request, 'End date must be grater than start date.')
                form = ArrangementForm(request.POST, request.FILES)
            else:
                obj = form.save(commit=False)
                obj.agency = AgencyUser.objects.get(id=request.user.id)
                obj.save()
                messages.success(request, 'Arrangement successfully created!')
                return redirect('home')

        else:
            messages.error(request, 'There was an issue while creating the arrangement!')
            form = ArrangementForm(request.POST, request.FILES)
    context = {'form': form}
    return render(request, 'base/arrangement_form.html', context)


@login_required(login_url='login')
@user_is_agency
def update_arrangement(request, pk):
    try:
        arrangement = Arrangement.objects.get(id=pk)
    except Arrangement.DoesNotExist:
        raise Http404("Given arrangement does not exist!")

    form = ArrangementForm(instance=arrangement)

    if request.method == 'POST':
        form = ArrangementForm(request.POST, request.FILES, instance=arrangement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Arrangement successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'There was an issue while updating the arrangement!')
            form = ArrangementForm(request.POST, request.FILES, instance=arrangement)
    context = {'form': form}
    return render(request, 'base/arrangement_form.html', context)


@login_required(login_url='login')
@user_is_agency
def delete_arrangement(request, pk):
    try:
        arrangement = Arrangement.objects.get(id=pk)
    except Arrangement.DoesNotExist:
        raise Http404("Given arrangement does not exist!")
    if request.method == 'POST':
        arrangement.delete()
        messages.success(request, 'Arrangement successfully deleted!')
        return redirect('home')
    else:
        messages.error(request, 'There was an issue while deleting the arrangement!')
    return render(request, 'base/delete.html', {'obj': arrangement})


@login_required(login_url='login')
@user_is_tourist
def reserve_arrangement(request, pk):
    page = 'reserve_arrangement'
    try:
        arrangement = Arrangement.objects.get(id=pk)
    except Arrangement.DoesNotExist:
        raise Http404("Given arrangement does not exist!")

    if request.method == 'POST':
        number_of_seats = request.POST.get('seats')
        if number_of_seats.isnumeric():
            number_of_seats = int(number_of_seats)
            if arrangement.number_of_free_seats < number_of_seats:
                messages.error(request, 'There are fewer free seats that requested.')
            else:
                arrangement.number_of_free_seats = arrangement.number_of_free_seats - number_of_seats
                tourists = arrangement.tourists.all()
                user = TouristUser.objects.get(id=request.user.id)
                arrangement.tourists.add(user)
                arrangement.save()
                if number_of_seats <= 3:
                    messages.info(request, 'Arrangement reserved! Total price of this arrangement is {} euros.'.format(
                        arrangement.price_per_person * number_of_seats))
                else:
                    price = 3 * arrangement.price_per_person + (
                            number_of_seats - 3) * (arrangement.price_per_person - arrangement.price_per_person * 0.1)
                    messages.info(request,
                                  'Arrangement reserved! Total price of this arrangement is {} euros.'.format(price))
                arrangement.save()
    return render(request, 'base/reserve_seat.html', {'page': reserve_arrangement})


@login_required(login_url='login')
def update_user(request):
    user = request.user
    if user.user_type == 'AGENCY':
        user = AgencyUser.objects.get(id=request.user.id)
        form = AgencyUserEditForm(instance=user)

        if request.method == 'POST':
            form = AgencyUserEditForm(request.POST, request.FILES, instance=user)

    else:
        user = TouristUser.objects.get(id=request.user.id)
        form = TouristUserEditForm(instance=user)

        if request.method == 'POST':
            form = TouristUserEditForm(request.POST, instance=user)

    if form.is_valid():
        user = form.save()
        user.save()
        messages.success(request, 'User successfully updated!')
        return redirect('home')
    else:
        messages.error(request, 'There was an issue while updating the user!')

    return render(request, 'base/update-user.html', {'form': form})

#     messages.success(request, 'Arrangement successfully updated!')
#     return redirect('home')
#
# else:
# messages.error(request, 'There was an issue while updating the arrangement!')
# form = ArrangementForm(request.POST, request.FILES, instance=arrangement)
