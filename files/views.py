from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ManagerForm
from . import paillier, AESCipher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from .models import Employee, Medicine, Component
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
            aes_key = AESCipher.gen_key()
            a = priv.get_list()
            priv1 = a[0]
            priv2 = a[1]
            file_key = password

            while len(file_key) != 32:
                file_key = file_key + str(random.randint(0,9))
            file_key = file_key.encode('UTF-8')
            print()
            print("pub " + str(type(pub)) + " " + str(pub))
            print("priv1 " + str(type(priv1)))
            print("priv2 " + str(type(priv2)))
            print("aes_key " + str(type(aes_key)) + " " + str(aes_key))
            print()
            f = open("manager.txt","w+")
            f.write(str(pub) + "\n")
            f.write(str(priv1) + "\n")
            f.write(str(priv2) + "\n")
            f.write(aes_key.hex())
            f.close()
            # AESCipher.encrypt_file(file_key, 'manager.txt')
            # AESCipher.decrypt_file(file_key, 'manager.txt.enc')

            f = open("employee.txt","w+")
            f.write(str(pub) + "\n")
            f.write(aes_key.hex())
            f.close()
            login(request, authenticate(username=username, password=password))

            return redirect('/addEmployee/')
    else:
                user_form = ManagerForm()

    return render(request,'files/managerRegister.html', {'user_form': user_form})               

def addEmployee(request):       
    return render(request,'files/addEmployee.html')

def display(request):
    file = open('manager.txt')
    all_lines = file.readlines() 
    pub = int(all_lines[0])
    print("display: " + str(pub))
    priv1 = int(all_lines[1])
    priv2 = int(all_lines[2])
    aes = all_lines[3]
    # aes = aes[2:-1]
    aes = bytes.fromhex(aes) 
    print(aes)
    values = []
    comp = Component.objects.all()
    for item in comp: 
        comp_name = item.component_name
        print("here")
        print(comp_name)
        # comp_name = bytes(comp_name, 'UTF-8')
        # comp_name = comp_name[2:-1]
        print(type(comp_name))
        comp_name = bytes.fromhex(comp_name)
        # comp_name = comp_name.encode('utf8')
        print(type(comp_name))
        # comp_name = comp_name.decode('UTF-8')
        # print(type(comp_name))
        print(comp_name)
        # print(type(comp_name))

        name = AESCipher.decrypt(aes, comp_name)
        quantity = paillier.decrypt(priv1, priv2, pub, int(item.component_quantity)) 
        cost = paillier.decrypt(priv1, priv2, pub, int(item.component_cost)) 
        print(name + " " + str(quantity) + " " + str(cost))
        # value = [name, quantity, cost]
        values.append(name)

    return render(request, 'files/display.html', {'name':values})

def medicineName(request):
    return render(request, 'files/medicineName.html')    

def addComponent(request):
    if request.method == 'POST':
        name = request.POST['inputName']
        quantity = request.POST['inputQuantity']
        cost = request.POST['inputCost']

        file = open('employee.txt')
        all_lines = file.readlines()
        pub_key = int(all_lines[0])
        aes_key = all_lines[1]
        # print(str(pub_key) + " " + aes_key)      
        # aes_key = aes_key[2:-1]
        aes_key = bytes.fromhex(aes_key) 
        # print(aes_key) 
        new_name = AESCipher.encrypt(name, aes_key)
        print("encrypted text in bytes: " + str(new_name))
        new_name = new_name.hex()
        print("encrypted name: " + new_name)        
        new_quantity = paillier.encrypt(pub_key, int(quantity))
        new_cost= paillier.encrypt(pub_key, int(cost))    
        # print(new_name + " " + str(new_quantity) + " " + str(new_cost))
        if Component.objects.filter(component_name=new_name).exists():
            obj = Component.objects.get(component_name=new_name)
            obj.component_quantity = paillier.e_add(pub_key, int(obj.component_quantity), int(new_quantity))
            obj.component_cost = paillier.e_add(pub_key, int(obj.component_cost), int(new_cost))
            obj.save()
        else:
            form = Component.objects.create(component_name=new_name, component_quantity=new_quantity, component_cost=new_cost)
            form.save() 
        return render(request, 'files/employee.html')              

    return render(request, 'files/employee.html')

# def register(request):
#     medicine_name = "Crocin"
#     file = open('manager.txt')
#     all_lines = file.readlines()
#     key = all_lines[3]
#     key = key[2:-1]
#     key = key.encode('UTF-8')
#     encrypt_msg = AESCipher.encrypt(medicine_name, key)

#     return HttpResponse("<h1>Holla modamustfakaa</h1>")

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
