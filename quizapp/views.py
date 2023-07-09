from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.db.models.query import QuerySet
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.validators import validate_email
from .models import Category,Questions,Options,correctopt,useropt,testtaken
# Create your views here.
# index method
def index(request):
    return render(request,'index.html')

# logout method

def logout(request):
    auth.logout(request)
    return redirect('/')

# login method

def login(request):
    if request.method=='POST':
        Username=request.POST['Username']
        Password=request.POST['Password']
        user=auth.authenticate(username=Username,password=Password)
        if user is not None:
            auth.login(request,user)
            messages.info(request,'Successfully logged in')
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
        
    return render(request,'login.html')

# register method

def register(request):
    if request.method=='POST':
        Username=request.POST['Username']
        email=request.POST['email']
        Password1=request.POST['Password1']
        Password2=request.POST['Password2']
        if len(Username)<6:
            messages.info(request,'username must be atleat 6 characters')
            return redirect('register')
        if len(Password1)<8:
            messages.info(request,'password should be atleat 8 characters')
            return redirect('register')
        try:
            validate_email(email)
        except:
            messages.info(request,'enter valid email')
            return redirect('register')
        if Password1==Password2:
            if User.objects.filter(username=Username).exists():
                messages.info(request,'Username is already taken') 
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('register')
            else:   
                user=User.objects.create_user(username=Username,password=Password1,email=email)
                user.save()
                messages.info(request,'user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
       
    return render(request,'register.html')

# home method

def home(request):
    return render(request,'home.html')

#dsquiz method
def quiz(request,cid):
    if request.method=='POST':
        count=0
        count1=0
        id2=Category.objects.get(id=cid)
        que=Questions.objects.filter(Catid=cid)
        userid=request.user.id
        id3=User.objects.get(id=userid)
        for q in que:
            uopt=request.POST.get(str(q.id))
            uopt1id=Options.objects.get(id=uopt)
            usopt=useropt.objects.create(qcat=id2,uid=id3,uqid=q,uoid=uopt1id)
            usopt.save()
            copt=correctopt.objects.filter(qid=q).values_list('oid',flat=True)
            if correctopt.objects.filter(oid=uopt1id):
                count+=1
            else:
                count1+=1
        percentage=round((count/(count+count1))*100,2)
        tt=testtaken.objects.create(tuid=id3,tcat=id2,tper=percentage)
        return render(request,'marks.html',{'count':count,'count1':count1,'percentage':percentage,'cid':cid})
            
    quest=Questions.objects.filter(Catid=cid)
    id = Questions.objects.filter(Catid=cid).values_list('id')
    options=Options.objects.filter(qid__in=id)
    oid=Options.objects.filter(qid__in=id).values_list('id')
    cortopt=correctopt.objects.filter(oid__in=oid)
    return render(request,'dsquiz.html',{'quest':quest,'options':options,'correctopt':cortopt,'cid':cid})
#user profile
def profile(request,uid):
    if request.method=='POST':
        fullname=request.POST['fullname']
        username=request.POST['username']
        password=request.POST.get('password') 
        if len(username)<6:
            messages.error(request,'username must be atleat 6 characters')
            return redirect('profile',uid)
        if User.objects.filter(username=username).exclude(id=uid).exists():
            messages.error(request,'Username is already taken') 
            return redirect('profile',uid)
        users=User.objects.filter(id=uid).update(first_name=fullname,username=username)
        if password==None:
            password=User.password
        else:
            if len(password)<8:
                messages.error(request,'password should be atleat 8 characters')
                return redirect('profile')  
            u = User.objects.get(id=uid)
            u.set_password(password)
            u.save()
            messages.success(request,'Password updated')
            return redirect('/')
        messages.success(request,'Successfully updated')
        return redirect('profile',uid)

    user=request.user
    uid=request.user.id
    da=testtaken.objects.filter(tuid=uid)
    query=testtaken.objects.filter(tuid_id=uid).query
    query.group_by=['tdate']
    result=QuerySet(query=query,model=testtaken)
    # result=testtaken.objects.filter(tuid_id=uid)
    result1=testtaken.objects.filter(tuid_id=uid).values('tdate').annotate(Count('id')).order_by()
    return render(request,'profile.html',{'user':user,'uid':uid,'result':result,'result1':result1})

#adding questions by user
def add(request,cid):
    if request.method=='POST':
        question=request.POST['question']
        option1=request.POST['option1']
        option2=request.POST['option2']
        option3=request.POST['option3']
        option4=request.POST['option4']
        correctoption=request.POST['correctoption']
        if correctoption=='1':
            crtopt=option1
        elif correctoption=='2':
            crtopt=option2
        elif correctoption=='3':
            crtopt=option3
        else:
            crtopt=option4
        if Questions.objects.filter(Question=question).exists():
            messages.info(request,'Question aready exists')
            return redirect('add')
        id1=Category.objects.get(id=cid)
        quest=Questions.objects.create(Question=question,Catid=id1)
        id=Questions.objects.filter(Question=question).values_list('id',flat=True)
        quest.save()
        opt=Options.objects.create(option=option1,qid_id=id)
        opt1=Options.objects.create(option=option2,qid_id=id)
        opt2=Options.objects.create(option=option3,qid_id=id)
        opt3=Options.objects.create(option=option4,qid_id=id)
        oid=Options.objects.filter(option=crtopt).values_list('pk',flat=True)
        opt.save()
        opt1.save()
        opt2.save()
        opt3.save()
        copt=correctopt.objects.create(oid_id=oid,qid_id=id)
        copt.save()
        return redirect('home')
    return render(request,'add.html',{'cid':cid})
# correct answers method

def correct(request,cid):
    rank=0
    quest=Questions.objects.filter(Catid=cid)
    id = Questions.objects.filter(Catid=cid).values_list('id')
    options=Options.objects.filter(qid__in=id)
    oid=Options.objects.filter(qid__in=id).values_list('id')
    cortopt=correctopt.objects.filter(oid__in=oid)
    correctoption=correctopt.objects.filter(oid__in=oid).values_list('oid_id')
    return render(request,'correct.html',{'quest':quest,'options':options,'cortopt':cortopt,'cid':cid})
