from django.shortcuts import render, redirect
from api.crm import getAllUsers, User


def index(req):
    return render(req, 'contacts/index.html', {'users': getAllUsers()})


def addContact(req):
    firstName = req.POST.get("firstName")
    lastName = req.POST.get("lastName")
    phoneNumber = req.POST.get("phoneNumber")
    address = req.POST.get("address")

    user = User(firstName=firstName,
                lastName=lastName,
                phoneNumber=phoneNumber,
                address=address)
    user.save()
    return redirect('index')


def deleteContact(req):
    firstName = req.POST.get("firstName")
    lastName = req.POST.get("lastName")
    user = User(firstName=firstName,
                lastName=lastName)
    user.delete()
    return redirect('index')
