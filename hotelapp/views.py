from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

current_datetime = timezone.now()
@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'admin_pages/inbox.html', {'messages': messages})

@login_required
def compose(request):
    if request.method == 'POST':
        receiver = User.objects.get(username=request.POST['receiver'])
        message = Message(sender=request.user, receiver=receiver, content=request.POST['content'])
        message.save()
        return redirect('inbox')
    else:
        return render(request, 'admin_pages/compose.html')
@login_required
def inboxGuest(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'guest_pages/inbox.html', {'messages': messages})

@login_required
def composeGuest(request):
    if request.method == 'POST':
        receiver = User.objects.get(username="admin")
        message = Message(sender=request.user, receiver=receiver, content=request.POST['content'])
        message.save()
        return redirect('home')
    else:
        return render(request, 'guest_pages/compose.html')
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('room_list')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
@login_required
def login_out(request):
    logout(request)
    return redirect('login')
def notify(request):

    return render(request, 'guest_pages/notify.html')
@login_required
def admin(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = RegistrationForm()
    context = {
        "form": form,
        "users":users
    }
    if request.user.is_superuser:
        return render(request, 'admin_pages/users.html',context)
    else:
        return HttpResponse("Can't access this page")
def deleteUsers(request,id):
    user = User.objects.get(id=id)
    if request.method =="POST":
        user.delete()
        return redirect('users_list')
def updateUsers(request,id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = RegistrationForm(instance=user)
    
    return render(request, 'admin_pages/update_user.html', {'form': form})
    
@login_required
def reservation(request):
    reserved = Reservation.objects.all()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            changeStatus(request)
            return redirect('reservation')
    else:
        form = ReservationForm()
    context = {
        "reserved":reserved,
        "form":form
    }
    if request.user.is_superuser:
        return render(request, 'admin_pages/reservations.html',context)
    else:
        return HttpResponse("Can't access this page")
def changeStatus(request):
    rooms = Room.objects.all()
    roomrelate = Reservation.objects.select_related("room").all()
    context = {
        "date":current_datetime
    }
    for room in rooms:
        is_available = True
        for reservation in roomrelate:
            if room.room_name == reservation.room.room_name and (reservation.start_date.date() <= current_datetime.date() and current_datetime.date() <= reservation.end_date.date()):
                is_available = False
                break
        room.is_available = is_available
        room.save()
def statusAvailable(request):
    rooms = Room.objects.all()
    roomrelate = Reservation.objects.select_related("room").all()
    for room in rooms:
        is_available = False
        for reservation in roomrelate:
            if room.room_name == reservation.room.room_name and (reservation.start_date.date() <= current_datetime.date() and current_datetime.date() > reservation.end_date.date()):
                is_available = True
                break
        if room.is_available is False:
            room.is_available = is_available
            room.save()
@login_required
def room(request):
    rooms = Room.objects.all()
    roomrelate = Reservation.objects.select_related("room").all()
    ## function to check the availability of a room on page load
    statusAvailable(request)

    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    for reservation in roomrelate:
        if reservation.end_date.date() < current_datetime.date():
            del reservation
    context = {
        "form": form,
        "rooms": rooms,
        "current_datetime":current_datetime,
        "roomsquery": roomrelate
    }
    if request.user.is_superuser:
        return render(request, 'admin_pages/room.html',context)
    else:
        return HttpResponse("Can't access this page")
def deleteReserve(request,id):
    reserve = Reservation.objects.get(id=id)
    roomrelate = Reservation.objects.select_related("room").all()
    rooms = Room.objects.all()
    for room in rooms:
        is_available = False
        for reservation in roomrelate:
            if reserve == reservation:
                is_available = True
        room.is_available = is_available
        room.save()
    reserve.delete()
    if request.user.is_superuser:
        return redirect('room_list')
    return redirect('home')
def deleteRoom(request,id):
    room = Room.objects.get(id=id)
    if request.method =="POST":
        room.delete()
        return redirect('room_list')
def updateRoom(request,id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES,instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'admin_pages/update_room.html', {'form': form})
def updateReserve(request,id):
    reserve = Reservation.objects.get(id=id)
    if request.method == 'POST':
        form = GuestReservationForm(request.POST,instance=reserve)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GuestReservationForm(instance=reserve)
    
    return render(request, 'guest_pages/update_reserve.html', {'form': form})
@login_required
def guestReservation(request):
    reserve = Reservation.objects.filter(username=request.user)
    context = {
        "reserve": reserve
    }
def home(request):
    reservation = Reservation.objects.filter(username=request.user)
    # expiration_period = timedelta(days=1)
    for reserve in reservation:
        if current_datetime.date() == reserve.end_date.date():
            messages.warning(request,f"Your Booking for room {reserve.room} expires today do you want to renew reservation")
    context = {
        "reservation":reservation,
        "current_datetime": current_datetime
    }
    return render(request, 'guest_pages/home.html',context)
def rooms(request):
    rooms = Room.objects.all()
    roomrelate = Reservation.objects.select_related("room").all()
     ## function to check the availability of a room on page load
    statusAvailable(request)
    context = {
        "rooms": rooms,
        "roomrelate": roomrelate
    }
    return render(request, 'guest_pages/rooms.html',context)

def bookRoom(request):
    selected_room_id = request.session.get('selected_room_id')
    room = get_object_or_404(Room,id=selected_room_id)
    form = GuestReservationForm(initial={'room': room})
    if request.method == 'POST':
        form = GuestReservationForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.username = request.user
            booking.room = room
            extra_services = form.cleaned_data['extra_services']
            booking.save()
            booking.extra_services.set(extra_services)
            changeStatus(request)
            del request.session['selected_room_id']
            return redirect('rooms')
    else:
        form = GuestReservationForm()
    context = {"form":form}
    return render(request, 'guest_pages/book_room.html',context)
def guestBookRoom(request,id):
    room = get_object_or_404(Room,id=id)
    request.session['selected_room_id'] = room.id

    return redirect("bookroom")
