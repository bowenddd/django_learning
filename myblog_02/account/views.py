from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import LoginForm,RegistrationForm, UserProfileForm, UserForm, UserInfoForm
from .models import UserInfo, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def user_login(request):
    print(request)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            form = login_form.cleaned_data
            user = authenticate(username=form['username'], password=form['password'])
            if user:
                login(request, user)
                return HttpResponse('Login successfully!')
            else:
                info = 'Sorry Your username or password is not right'
                return render(request, 'account/login.html', {'form':login_form,'info':info})
        else:
            info = 'Invalid Format'
            return render(request, 'account/login.html', {'form': login_form, 'info': info})

    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form':login_form})


def register(request):
    if request.method =='POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponseRedirect(reverse('account:user_login'))

        else:
            return HttpResponse('Sorry You can not Register!')

    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request,'account/register.html',{'form':user_form,'profile':userprofile_form})

@login_required()
def myself(request):
    if request.method =='POST':
        return HttpResponseRedirect('/account/edit-my-information/')
    else:
        userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,'userprofile') else UserProfile.objects.create(user=request.user)
        userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,'userinfo') else UserInfo.objects.create(user=request.user)

        return render(request,'account/myself.html',{'userprofile':userprofile,'userinfo':userinfo,'user':request.user})

@login_required()
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user,
                                                                        'userprofile') else UserProfile.objects.create(
        user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,
                                                                  'userinfo') else UserInfo.objects.create(
        user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data

            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            userinfo.profession = userinfo_cd['profession']
            userinfo.company = userinfo_cd['company']
            userinfo.school = userinfo_cd['school']

            request.user.save()
            userinfo.save()
            userprofile.save()

            return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={
            'birth':userprofile.birth,
            'phone':userprofile.phone
        })
        userinfo_form = UserInfoForm(initial={
            'profession':userinfo.profession,
            'company':userinfo.company,
            'school':userinfo.school,
            'address':userinfo.address,
            'aboutme':userinfo.aboutme,
        })
        return render(request,'account/myself_edit.html',{
           'user_form':user_form,
           'userinfo':userinfo_form,
           'userprofile':userprofile_form,
            'userphoto':userinfo.photo
        })

def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user,
                                                                      'userinfo') else UserInfo.objects.create(
            user = request.user
        )
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)