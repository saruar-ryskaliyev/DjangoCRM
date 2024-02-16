from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):

    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in!')
            return redirect('home')

    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have been successfully registered!")

            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):

    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': record})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


def customer_record_delete(request, pk):
    if request.user.is_authenticated:
        to_delete = Record.objects.get(id=pk)
        to_delete.delete()
        messages.success(request, "Deleted")
        return redirect('home')
    else:
        messages.success(request, "Unable to delete")
        return redirect('home')


def add_record(request):

    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid:
            instance = form.save()
            instance.save()
            messages.success(request, "Record has been added")
            return redirect('home')
    else:
        form = AddRecordForm()
        return render(request, 'add_record.html', {'form': form})


    return render(request, 'add_record.html', {})


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        return render(request, 'update_record.html', {})