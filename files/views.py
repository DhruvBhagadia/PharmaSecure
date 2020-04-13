from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ManagerForm
from . import paillier, AESCipher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from .models import Employee, Medicine, Component, Log
from django.conf import settings
from django.core.mail import send_mail
import random, datetime
from django.contrib.auth.decorators import login_required


def employeeLogin(request):
    if request.method == 'POST':
        email = request.POST['email'] 
        password = request.POST['password']       
        if Employee.objects.filter(email=email).exists() and password=="password":
            element = Employee.objects.get(email=email)
            return redirect('/employee/' + str(element.id))
            # return redirect('addComponent', employee_id=element.id)

    return render(request, 'files/employeeLogin.html')

def newPassword(request):
    return render(request, 'files/newPassword.html')

def managerLogin(request):
    logout(request)
    if request.POST:
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/addEmployee/')

    return render(request, 'files/managerLogin.html')

def managerRegister(request):
    if request.method == 'POST':

        user_form = ManagerForm(request.POST)
        medicine = request.POST.get('medicine')
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
            medicine = AESCipher.encrypt(medicine,aes_key)
            medicine = medicine.hex()
            med = Medicine.objects.create(manager = user, medicine_name = medicine)
            med.save()
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
            #AESCipher.encrypt_file(password,'manager.txt')
            f = open("employee.txt","w+")
            f.write(str(pub) + "\n")
            f.write(aes_key.hex())
            f.close()
            #AESCipher.encrypt_file('password','employee.txt')
            login(request, authenticate(username=username, password=password))

            return redirect('/addEmployee/')
    else:
                user_form = ManagerForm()

    return render(request,'files/managerRegister.html', {'user_form': user_form})               



login_required(login_url='files:manLog')
def addEmployee(request):
    user = User.objects.get(username = request.user.username)
    med = Medicine.objects.get(manager = user)
    if request.method == 'POST':
        emp_name = request.POST['inputName']
        emp_email = request.POST['inputEmail3']
        print(emp_name)
        emp_obj = Employee.objects.create(email=emp_email,name=emp_name,manager_name = user.username,medicine_name = med.medicine_name )
        emp_obj.save()
        subject = "Important Notfication"
        message = 'Following is your username and password to login in DevMust Impex ' \
                  'Username: ' + emp_email + ' Password: password'
        from_email = settings.EMAIL_HOST_USER
        to_list = [emp_email,from_email]
        send_mail(subject=subject,from_email=from_email,message=message,recipient_list=to_list,fail_silently=True)
        return render(request, 'files/addEmployee.html')
    else:
        return render(request,'files/addEmployee.html')


login_required(login_url='files:manLog')
def logs(request):
    log = Log.objects.all()
    file = open('manager.txt')
    all_lines = file.readlines() 
    pub = int(all_lines[0])
    priv1 = int(all_lines[1])
    priv2 = int(all_lines[2])
    aes = all_lines[3]
    aes = bytes.fromhex(aes) 
    values = []

    ctr = 1
    for item in log: 
        comp_name = item.component_name
        comp_name = bytes.fromhex(comp_name)
        name = AESCipher.decrypt(aes, comp_name)
        quantity = paillier.decrypt(priv1, priv2, pub, int(item.component_quantity)) 
        cost = paillier.decrypt(priv1, priv2, pub, int(item.component_cost)) 
        value = {}
        value['ctr'] = ctr
        value['created'] = item.created
        value['ename'] = item.name
        value['cname'] = name
        value['quantity'] = quantity
        value['cost'] = cost
        values.append(value)
        ctr = ctr+1

    return render(request, 'files/logs.html', {'values': values})

login_required(login_url='files:manLog')
def display(request):
    file = open('manager.txt')
    all_lines = file.readlines() 
    pub = int(all_lines[0])
    priv1 = int(all_lines[1])
    priv2 = int(all_lines[2])
    aes = all_lines[3]
    aes = bytes.fromhex(aes) 
    #comp = Component.objects.all()
    user = User.objects.get(username = request.user)
    med = Medicine.objects.get(manager = user)
    comp = Component.objects.filter(key = med)

    med_name = med.medicine_name
    med_name = bytes.fromhex(med_name)
    med_name = AESCipher.decrypt(aes, med_name)
    values = []

    ctr = 1
    for item in comp: 
        comp_name = item.component_name
        comp_name = bytes.fromhex(comp_name)
        name = AESCipher.decrypt(aes, comp_name)
        quantity = paillier.decrypt(priv1, priv2, pub, int(item.component_quantity)) 
        cost = paillier.decrypt(priv1, priv2, pub, int(item.component_cost)) 
        value = {}
        value['ctr'] = ctr
        value['name'] = name
        value['quantity'] = quantity
        value['cost'] = cost
        values.append(value)
        ctr = ctr+1

    return render(request, 'files/display.html', {'values':values, 'med_name': med_name})

def medicineName(request):
    return render(request, 'files/medicineName.html')    

login_required(login_url='files:empLog')
def addComponent(request, employee_id):

    element = Employee.objects.get(id=employee_id)
    medicine = Medicine.objects.get(medicine_name = element.medicine_name)
    file = open('employee.txt')
    all_lines = file.readlines()
    pub_key = int(all_lines[0])
    aes_key = all_lines[1]
    aes_key = bytes.fromhex(aes_key)

    med_name = medicine.medicine_name
    med_name = bytes.fromhex(med_name)
    med_name = AESCipher.decrypt(aes_key, med_name)

    if request.method == 'POST':
        employee_name = element.name
        date_field = datetime.datetime.now()
        name = request.POST['inputName']
        quantity = request.POST['inputQuantity']
        cost = request.POST['inputCost'] 

        new_name = AESCipher.encrypt(name, aes_key)
        new_name = new_name.hex()
        new_quantity = paillier.encrypt(pub_key, int(quantity))
        new_cost= paillier.encrypt(pub_key, int(cost)) 

        log = Log.objects.create(created=date_field, name = employee_name, component_name=new_name, component_quantity=new_quantity, component_cost=new_cost)
        log.save() 

        if Component.objects.filter(component_name=new_name).exists():
            obj = Component.objects.get(component_name=new_name)
            obj.component_quantity = paillier.e_add(pub_key, int(obj.component_quantity), int(new_quantity))
            obj.component_cost = paillier.e_add(pub_key, int(obj.component_cost), int(new_cost))
            obj.save()            
        else:
            form = Component.objects.create(key = medicine ,component_name=new_name, component_quantity=new_quantity, component_cost=new_cost)
            form.save() 
        # return render(request, 'files/employee.html')              

    return render(request, 'files/employee.html', {'employee':element, 'med_name': med_name})

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
