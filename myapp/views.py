from django.http import HttpResponse,HttpResponseRedirect
from .models import Topic, Course, Student
from django.shortcuts import get_object_or_404,render,redirect,reverse
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm, ForgotPasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
import string,random
from mysiteS21.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    courses_list = Course.objects.all().order_by('-title')[:5]
    return render(request,'myapp/index.html',{'top_list': top_list,'courses_list': courses_list})



def about(request):
    response = render(request, 'myapp/about.html')
    count = 1
    if 'about_visits' in request.COOKIES:
        print('if')
        count = int(request.COOKIES['about_visits']) + 1
        response.set_cookie('about_visits', str(count), max_age=10)
    else:
        print('else')
        response.set_cookie('about_visits', str(count), max_age=10)

    return response

def detail(request,pk):
    topic_detail = get_object_or_404(Topic,pk=pk)
    related_courses_list = Course.objects.filter(topic_id=pk).values()
    return render(request,'myapp/detail.html',{'topic_detail':topic_detail,'related_courses_list': related_courses_list})

def findcourses(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            if(length):
                topics = Topic.objects.filter(length=length)
            else:
                topics = Topic.objects.all()
            courselist = []
            for top in topics:
                courselist = courselist + list(top.courses.filter(price__lte=max_price))
            return render(request,'myapp/results.html',{'courselist': courselist,'name':name,'length':length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request,'myapp/findcourses.html',{'form': form})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.Student
            status = order.order_status
            order.save()
            form.save_m2m()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request,'myapp/order_response.html',{'courses':courses,'order': order})
        else:
            return render(request,'myapp/place_order.html',{'form':form})
    else:
        form = OrderForm()
        return render(request,'myapp/place_order.html',{'form':form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                reviewForm = form.save(commit=False)
                course = reviewForm.course
                reviewForm.save()
                course.num_reviews = course.num_reviews + 1
                course.save()
                return redirect('myapp:index')
            else:
                return render(request,'myapp/review.html',{'form': form,'message':'You must enter rating between 1 and 5'})
    else:
        form = ReviewForm()
        return render(request,'myapp/review.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if request.session.has_key('last_login'):
                    messages.success(request, 'Last Login Date and Time : ' + str(request.session['last_login']))
                else:
                    messages.success(request, 'Your last login was more than one hour ago')

                request.session['last_login'] = str(timezone.now())
                request.session['username'] = username
                request.session['user_first_name'] = user.first_name
                request.session['user_last_name'] = user.last_name
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request,'myapp/login.html')

@login_required(login_url='myapp:login')
def user_logout(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required(login_url='myapp:login')
def myaccount(request):
    if request.user.groups.filter(name='Student').exists():
        studentDetails = Student.objects.filter(pk=request.user)
        course = []
        reg_course = []
        for student in studentDetails:
            for co in student.registered_courses.all():
                course.append(co)

            for rg in student.interested_in.all():
                reg_course.append(rg)

        return render(request,'myapp/account.html',{'message':'', 'name':student.first_name+' '+student.last_name, 'course':course, 'reg_course':reg_course})
    else:
        return render(request,'myapp/account.html', {'message' : 'You are not a registered student!'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            userForm = form.save(commit=False)
            userForm.password = make_password(form.cleaned_data['password'])
            userForm.save()
            form.save_m2m()
            g = Group.objects.get(name='Student')
            g.user_set.add(userForm)
            return HttpResponseRedirect(reverse('myapp:index'))
        else:
            return HttpResponse('Error during registration')
    else:
        form = RegisterForm()
        return render(request,'myapp/register.html',{'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            random_password = ''.join(random.choice(string.ascii_letters) for i in range(10))
            password = make_password(random_password)
            Student.objects.filter(email=form.cleaned_data['Email']).update(password=password)

            subject = 'New Password'
            message = 'Your new password for E-learning site is ' + random_password
            recepient = form.cleaned_data['Email']
            send_mail(subject,message,EMAIL_HOST_USER,[recepient],fail_silently=False)
            return HttpResponse('A password has been sent to your inbox')
        else:
            return HttpResponse('Incorrect details')
    else:
        form = ForgotPasswordForm()
        return render(request,'myapp/forgot_password.html',{'form': form})







