from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from form import ProjectForm
from authentication.models import Project



def Signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            try:
                if User.objects.get(username=uname):
                    return HttpResponse("user already exist")
            except:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
        

    return render(request, 'signup.html')


def Login(request):
    print(request.session.session_key)
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


@login_required(login_url='login')
def Homepage(request):
    print(request.session.session_key)
    return render(request, 'home.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def createproject(request):
    return redirect('project')


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('create_project')  # Redirect to the home page
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects.html', {'projects': projects})