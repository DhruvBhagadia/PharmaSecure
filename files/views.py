from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ManagerForm
from . import paillier, AESCipher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from .models import Employee 
import random


def managerLogin(request):
    if request.method=='POST':

        user_form = ManagerForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            priv,pub = paillier.generate_keypair(256)
            aes = AESCipher.gen_key()
            a = priv.get_list()
            priv1 = a[0]
            priv2 = a[1]
            file_key = password

            while len(file_key) != 32:
                file_key = file_key + str(random.randint(0,9))
            file_key = file_key.encode('UTF-8')
            
            f = open("manager.txt","w+")
            f.write(str(pub) + "\n")
            f.write(str(priv1) + "\n")
            f.write(str(priv2) + "\n")
            f.write(str(aes))
            f.close()
            AESCipher.encrypt_file(file_key, 'manager.txt')
            AESCipher.decrypt_file(file_key, 'manager.txt.enc')
            # AESCipher.decrypt_file(file_key, '')

            f = open("employee.txt","w+")
            f.write(str(pub) + "\n")
            f.write(str(aes))
            f.close()
            login(request, authenticate(username=username, password=password))

            return redirect('/AddEmployee/')
    else:
                user_form = ManagerForm()

    return render(request,'files/login.html', {'user_form': user_form})               

def addEmployee(request):       
    return render(request,'files/addEmployee.html')

def register(request):
    medicine_name = "Crocin"
    file = open('manager.txt')
    all_lines = file.readlines()
    key = all_lines[3]
    key = key[2:-1]
    key = key.encode('UTF-8')
    encrypt_msg = AESCipher.encrypt(medicine_name, key)

    return HttpResponse("<h1>Holla modamustfakaa</h1>")

# def register_med(request):

#     if request.method =='POST':
#         medicine = Medicine(request.POST)
#         if medicine.is_valid():
#             medicine1 = medicine.save(commit=False)
#             priv,pub = paillier.generate_keypair(256)
#             a = priv.get_list()
#             priv1=a[0]
#             priv2 = a[1]
#             medicine1.privateKey_1 = priv1
#             medicine1.privateKey_2 = priv2
#             medicine1.publicKey = pub
#             medicine1.save()

#             return redirect('/home/')
#     else:
#         medicine = Medicine()
#     return render(request,'files/test.html',{'medicine':medicine})

# def add_component(request,med_id):
#     medic = Key.objects.get(id = med_id)
#     if request.method == 'POST':
#         constituent = Constituent(request.POST)
#         if constituent.is_valid():
#             constituent1 = constituent.save(commit=False)
#             quant = int(constituent1.component_quantity)
#             cost = int(constituent1.component_cost)
#             pub = int(medic.publicKey)
#             new_cost= paillier.encrypt(int(pub),cost)
#             new_quant = paillier.encrypt(pub,quant)
#             constituent1.component_quantity = new_quant
#             constituent1.component_cost = new_cost
#             constituent1.key = medic
#             constituent1.save()
#             return redirect('/home/')
#     else:
#         constituent = Constituent()
#     return render(request,'files/constituent.html',{'constituent':constituent,'medic':medic})

# def home(request):
#     items = Key.objects.all()

#     return render(request,'files/home.html',{'items':items})

# def retrieve_components(request,id):
#     medic = Key.objects.get(id = id)
#     compo = Component.objects.filter(key=medic)
#     a = {}
#     for c in compo:
#         c.component_cost = paillier.decrypt(int(medic.privateKey_1),int(medic.privateKey_2),int(medic.publicKey),int(c.component_cost))
#         c.component_quantity = paillier.decrypt(int(medic.privateKey_1), int(medic.privateKey_2), int(medic.publicKey),
#                                             int(c.component_quantity))
#         a[c.component_name] = [c.component_cost,c.component_quantity]

#     return render(request,'files/detail.html',{'a':a,'compo':compo})
