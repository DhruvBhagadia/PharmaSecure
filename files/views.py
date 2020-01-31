from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import Medicine,Constituent
from . import paillier
# Create your views here.
from .models import Key,Component
def test(request,id):
    com = Component.objects.filter(id =id)
    z = Component.objects.filter(component_name = com)

    return HttpResponse(
        "<h1>Holla MotherFucker</h1>"
    )

# def register(request):
#     medicine_name = 'Crocin'
#     priv,pub = paillier.generate_keypair(256)
#     a = priv.get_list()
#     priv1=a[0]
#     priv2 = a[1]
#     return render(request,'files/test.html',{'priv1':priv1,'priv2':priv2})

def register_med(request):

    if request.method =='POST':
        medicine = Medicine(request.POST)
        if medicine.is_valid():
            medicine1 = medicine.save(commit=False)
            priv,pub = paillier.generate_keypair(256)
            a = priv.get_list()
            priv1=a[0]
            priv2 = a[1]
            medicine1.privateKey_1 = priv1
            medicine1.privateKey_2 = priv2
            medicine1.publicKey = pub
            medicine1.save()

            return redirect('/home/')
    else:
        medicine = Medicine()
    return render(request,'files/test.html',{'medicine':medicine})

def add_component(request,med_id):
    medic = Key.objects.get(id = med_id)
    if request.method == 'POST':
        constituent = Constituent(request.POST)
        if constituent.is_valid():
            constituent1 = constituent.save(commit=False)
            quant = int(constituent1.component_quantity)
            cost = int(constituent1.component_cost)
            pub = int(medic.publicKey)
            new_cost= paillier.encrypt(int(pub),cost)
            new_quant = paillier.encrypt(pub,quant)
            constituent1.component_quantity = new_quant
            constituent1.component_cost = new_cost
            constituent1.key = medic
            constituent1.save()
            return redirect('/home/')
    else:
        constituent = Constituent()
    return render(request,'files/constituent.html',{'constituent':constituent,'medic':medic})

def home(request):
    items = Key.objects.all()

    return render(request,'files/home.html',{'items':items})

def retrieve_components(request,id):
    medic = Key.objects.get(id = id)
    compo = Component.objects.filter(key=medic)
    a = {}
    for c in compo:
        c.component_cost = paillier.decrypt(int(medic.privateKey_1),int(medic.privateKey_2),int(medic.publicKey),int(c.component_cost))
        c.component_quantity = paillier.decrypt(int(medic.privateKey_1), int(medic.privateKey_2), int(medic.publicKey),
                                            int(c.component_quantity))
        a[c.component_name] = [c.component_cost,c.component_quantity]

    return render(request,'files/detail.html',{'a':a,'compo':compo})
