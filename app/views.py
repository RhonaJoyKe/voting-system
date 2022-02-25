from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.core.paginator import Paginator
from django.db.models import Count
# Create your views here.
def home(request):
    
    return render(request, 'index.html')
def login_user(request):
    form = AuthenticationForm(request, data=request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!!",
                           extra_tags='alert alert-warning alert-dismissible fade show')
    form = AuthenticationForm()
    return render(request, 'registration/login.html',{'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request):
    if request.method == 'POST':
        check1 = False
        check2 = False
        check3 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password doesn\'t matched',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(email=email).exists():
                check3 = True
                messages.error(request, 'Email already registered',
                               extra_tags='alert alert-warning alert-dismissible fade show')

            if check1 or check2 or check3:
                messages.error(
                    request, "Registration Failed", extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                messages.success(
                    request, f'Thanks for registering {user.username}!', extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def candidate(request):


	candidates = Candidate.objects.all()
	if request.method == 'POST':
			form =CandidateForm(request.POST, request.FILES)
			if form.is_valid():
					post = form.save(commit=False)
					post.user = request.user
					post.save()
					return HttpResponseRedirect(request.path_info)
	else:
			form = CandidateForm()
	params = {
        'candidates':candidates,
				'form': form, 
       
        }
	return render(request, 'candidates.html', params)
def candidate_delete(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if request.user != candidate.admin:
        return redirect('home')
    candidate.delete()
    messages.success(request, "Candidate Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("")
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk = pos)
    if request.method == "POST":

        temp = Votes.objects.get_or_create(user=request.user, position=obj)[0]

        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/position/')
        else:
            messages.success(request, 'you have already  voted this position.')
            return render(request, 'candidate_list.html', {'obj':obj})
    else:
        return render(request, 'candidate_list.html', {'obj':obj})

def positionView(request):
    obj = Position.objects.all()
    return render(request, "positions.html", {'obj':obj})
def resultView(request):
    obj = Candidate.objects.all().order_by('position','-total_vote')
    return render(request, "results.html", {'obj':obj})

  