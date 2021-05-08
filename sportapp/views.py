from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.http import HttpResponse,Http404

from datetime import datetime


# Create your views here.
class sup:
    def __init__(self,iss,club,secy_name) :
        self.iss=iss
        self.club=club
        self.secy_name=secy_name

def Index(request):
    clubs_list=clubs.objects.all()
    context = {
            'clubs_list':clubs_list,
        }
    user = request.user
  
    if user.email=="n.kailash@iitg.ac.in":
        return render(request,'sportapp/home.html',context)
    else:
        clubs_list=clubs.objects.all()
        for club in clubs_list:
            if (str(club.email)==str(user.email)):
                return render(request,'sportapp/Secy_home.html',context)

       
    raise Http404("Page does not exist")


def ClubsView(request):
    
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Your club has been saved!')
            return redirect('clubsList')

    else:
        form = ClubForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_club.html', context)   
    
def UpdateClubsView(request,pk):
 if request.user.email=='superindent@iitg.ac.in' or request.user.email=='gensec@iitg.ac.in' :  
    if request.method == 'POST':
        form1 = ClubForm(request.POST)
        if form1.is_valid():
            form=form1.save(commit=False)
            clubs.objects.filter(pk=pk).update(name=form.name,secy_name=form.secy_name,email=form.email,dept=form.dept,prog=form.prog)
            return redirect('clubsList')

    else:
        club=clubs.objects.get(pk=pk)
        dict={
            "name":club.name,
            "secy_name":club.secy_name,
            "email":club.email,
            "dept":club.dept,
            "prog":club.prog
        }
        form = ClubForm(initial=dict)
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_club.html', context)   


        

class ClubsListView(ListView):
    model = clubs
    template_name = 'sportapp/clubs_list.html'

def EquipmentView(request,pk):
   if request.user.email=='n.kailash@iitg.ac.in' or request.user.email=='gensec@iitg.ac.in' :  
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity
            post.sport=clubs.objects.get(pk=pk)
            post.save()
            messages.success(request,f'Your Equipment has been saved!')
            return redirect('equipmentsList',pk=pk)
    else:
            
        form = EquipmentForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_equipment.html', context)       
        
           
def EquipmentListView(request,pk):

    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    c=club.name
    superin=0
    gensec=0
    
    if request.user.email=='bteja@iitg.ac.in'    :
      superin=1
    if request.user.email== 'n.kailash@iitg.ac.in' :
      
      gensec=1 
    
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments,
            'c':c,
            'super':superin,
            'gensec':gensec
        }
    return render(request, 'sportapp/equipments_list.html', context)      



def deleteEquipmentView(request,id,pk):
    if request.user.email=='n.kailash@iitg.ac.in' or request.user.email=='gensec@iitg.ac.in' :
     a=equipment.objects.filter(id=id)
     a.delete()
     return redirect('equipmentsList',pk=pk)


def IssueFormView(request,pk,id):
    equip=get_object_or_404(equipment, id=id)
   
    if request.method == 'POST':

        form = IssueForm(request.POST)
        if form.is_valid():
         post = form.save(commit=False)
            
         quantity = equip.available_quantity-post.quantity
         post.equipment_name= equip
         post.remark=None
         post.save()
        
         return redirect('IssueList',pk=pk)  

    else:
        equip=get_object_or_404(equipment, id=id)
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
        }
        return render(request, 'sportapp/Issue.html', context)      



def IssueListView(request,pk):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    tot_list=issue.objects.all()
    print(tot_list)
    issue_list=[]
    
    for equip in equipments:
        for o in tot_list:
            if str(o.equipment_name) == str(equip.name):
                issue_list.append(o)
    issue_list.reverse()  
          
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
        }
    return render(request, 'sportapp/Issue_list.html', context)

def returnequipment(request,pk,id):
    if request.method == 'POST':
        eq=get_object_or_404(equipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            post.remark=None
            iss=issue(name=post.name,equipment_name=eq,roll=post.roll,quantity=quan,is_return=True)
            iss.save()
            return redirect('IssueList',pk=pk)  

    else:
        form = ReturnForm()
        eq=get_object_or_404(equipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
        return render(request, 'sportapp/return_form.html', context)    

def superindent(request):
    user = request.user
    if user.email=="n.kailash@iitg.ac.in":
        iss=issue.objects.filter(is_pending=True)
        context={'iss':iss}
        
        suplist=[]
        for i in range(len(iss)):
            if iss[i].equipment_name :
                p=iss[i].equipment_name.sport.name
                q=iss[i].equipment_name.sport.secy_name
                p1=sup(iss[i],p ,q )
                suplist.append(p1)
            else:
                suplist.append(sup(iss[i],"general","general"))

       
        context={'iss':suplist}
        

        return render(request,'sportapp/superindent.html',context)
    else:
        return redirect('Home')

def accept(request,pk):
   if request.method=='POST': 
    form=remarkform(request.POST)
    if form.is_valid:
        post=form.save(commit=False)
    issue.objects.filter(pk=pk).update(is_pending=False,req=True,date=datetime.now(),remark=post.remark)
    isl=issue.objects.get(pk=pk)
    
    
    if isl.equipment_name:
       ik=isl.equipment_name.id
       eq=equipment.objects.get(pk=ik)
       if isl.is_return==False:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity-isl.quantity)
        
       if isl.is_return==True:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity+isl.quantity)
    else :
       ik=isl.general_equipname.id 
       eq=generalequipment.objects.get(pk=ik)  
       if isl.is_return==False:
        generalequipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity-isl.quantity)
        
       if isl.is_return==True:
        generalequipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity+isl.quantity)
    
          
         

    return redirect('superindent')
   
   else: 
     form=remarkform()
     return render(request,'sportapp/remarkform.html',{'form':form})  
    

def deny(request,pk):
 if request.method=='POST': 
    form=remarkform(request.POST)
    if form.is_valid:
        post=form.save(commit=False)
    issue.objects.filter(pk=pk).update(is_pending=False,date=datetime.now(),remark=post.remark)
    return redirect('superindent')
 else :
    form=remarkform()
    return render(request,'sportapp/remarkform.html',{'form':form}) 

def secyEquipments(request):
    user = request.user
    clubs_list=clubs.objects.all()
    for club in clubs_list:
        if (str(club.email)==str(user.email)):
            club=clubs.objects.get(pk=club.pk)
            equipments=club.equipment_set.all()
            tot_list=issue.objects.all()
            issue_list=[]
            for equip in equipments:
                for o in tot_list:
                    if (str(o.equipment_name) == str(equip.name)):
                        issue_list.append(o)

            context = {
            'issue_list':issue_list,
            'equipments':equipments,
            'pk':club.pk,
            'club':club,
            }     
            return render(request, 'sportapp/secy.html', context)   

    raise Http404("Page does not exist")


def secyIssueList(request):
    user = request.user
    clubs_list=clubs.objects.all()
    for club in clubs_list:
        if (str(club.email)==str(user.email)):
            club=clubs.objects.get(pk=club.pk)
            equipments=club.equipment_set.all()
            tot_list=issue.objects.all()
            issue_list=[]
            for equip in equipments:
                for o in tot_list:
                    if (str(o.equipment_name) == str(equip.name)):
                        issue_list.append(o)

            context = {
            'issue_list':issue_list,
            'equipments':equipments,
            'club':club,
            }     
            return render(request, 'sportapp/secy_issue.html', context)   

    raise Http404("Page does not exist")


    

def SecyEquipmentView(request,pk):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity
            post.sport=clubs.objects.get(pk=pk)
            post.save()
            messages.success(request,f'Your Equipment has been saved!')
            return redirect('Secy')
    else:
            
        form = EquipmentForm()
        context = {
            'form':form,
        }
        return render(request, 'sportapp/add_equipment.html', context)               

def SecyIssueFormView(request,pk,id):
    equip=get_object_or_404(equipment, id=id)
    if request.method == 'POST':

        form = IssueForm(request.POST)
        if form.is_valid():
         post = form.save(commit=False)
            # if post.quantity > equip.available_quantity:
            #     return HttpResponse('Cannot be issued')
            # else:   
         quantity = equip.available_quantity-post.quantity
         post.equipment_name= equipment.objects.get(id=id)
         post.save()

         return redirect('SecyIssueList')  

    else:
        equip=get_object_or_404(equipment, id=id)
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
        }
    return render(request, 'sportapp/Issue.html', context)      

def SecyDeleteEquipmentView(request,id,pk):
    a=equipment.objects.filter(id=id)
    a.delete()
    return redirect('Secy')
         
def Secyreturnequipment(request,pk,id):
    if request.method == 'POST':
        eq=get_object_or_404(equipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            iss=issue(name=post.name,equipment_name=eq,roll=post.roll,quantity=quan,is_return=True)
            iss.save()
            return redirect('SecyIssueList')  

    else:
        form = ReturnForm()
        eq=get_object_or_404(equipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
        return render(request, 'sportapp/return_form.html', context)             

class TotalListView(ListView):
    model=issue
    template_name='sportapp/Total_list.html'

def general(request):
    clubs_list=clubs.objects.all()
    equipments=generalequipment.objects.all()
    superin=0
    gensec=0
    
    if request.user.email=='bteja@iitg.ac.in'    :
      super=1
    if request.user.email== 'bkartheek@iitg.ac.in' :
      
      gensec=1 
    
    context = {
             'clubs_list': clubs_list,
            'equipments':equipments,
            'super':superin,'gensec':gensec
        }
    return render(request,'sportapp/general.html',context)
def addgeneral(request):
    if request.method == 'POST':
        form = generalequipmentform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity
            post.save()
            return redirect('general')
    else:       
        form = generalequipmentform()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_equipment.html', context)
def generalissue(request,pk):
    equip=get_object_or_404(generalequipment, pk=pk)
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            quantity = equip.available_quantity-post.quantity
            post.general_equipname=equip
            post.remark=None
            post.save()
            return redirect('general')  
    else:
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
        }
    return render(request, 'sportapp/Issue.html', {'form':form,'maximum_value':equip.available_quantity})      

def generallist(request):
     
    iss=issue.objects.filter(equipment_name=None)
    context={'issue_list':iss}
    return render(request,'sportapp/Issue_list.html',context)


def generalreturn(request,id):
    if request.method == 'POST':
        eq=get_object_or_404(generalequipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            post.remark=None
            iss=issue(name=post.name,general_equipname=eq,roll=post.roll,quantity=quan,is_return=True)
            iss.save()
            return redirect('generalIssueList')  
    else:
        form = ReturnForm()
        eq=get_object_or_404(generalequipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
        return render(request, 'sportapp/return_form.html', context)
def generaldelete(request,id):
    a=generalequipment.objects.get(pk=id)
    a.delete()
    return redirect('general')        