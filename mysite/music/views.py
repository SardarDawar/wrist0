from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import loginForm, registerForm, EditProfileForm, profileInformForm, contactForm,InformationForm,InformationFormEdit
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import profileModel,Information
from django.db.models import Q
from django.urls import reverse

def handler404(request):
    return render(request, '404.html', status=404)

def home(request):
    return render(request, 'music/home.html', )

@login_required()
def dashboard(request,user_name):
   
    user=User.objects.get(username=user_name)        
    data=Information.objects.filter(user=user)
  
    
    context={
        'data':data,
     
    }
    return render(request, 'music/dashboard.html',context)

def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard', args=[request.user.username])) 
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    return render(request, 'music/login.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required()
def profile_user(request, user_name):
    message = ''
    try:
        user = User.objects.get(username = user_name)
        editProfile = False
        #print(request.user.username == user_name)
        if (request.user==user):
            if request.user.is_superuser:
                contactNumber = None
                editProfile = True
            else:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = True
        else:
            if request.user.is_superuser:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = False
            else:
                contactNumber = None
                editProfile = None
    except:
        user=request.user
        if request.user.is_superuser:
            contactNumber = None
            editProfile = True
            message = user_name + " Doest Not Exists "
        else:
            contactNumber  = profileModel.objects.get(user = User.objects.get(username = request.user.username)).contactNumber
            editProfile = True
            message = user_name
    return render(request, 'music/profile.html', {'contactNumber': contactNumber,'editProfile' :editProfile, 'user':user, 'message' : message})
    
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email'].lower()
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.city = form_2.cleaned_data['city']
            profile.county = form_2.cleaned_data['county']
            profile.state = form_2.cleaned_data['state']
            profile.country = form_2.cleaned_data['country']
            profile.continent = form_2.cleaned_data['continent'] 
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('music/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email').lower()
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'music/acc_active_email_confirm.html')
    return render(request, 'music/register.html', {'form' : form, 'form_2' : form_2})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required()
def edit_profile(request):
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/edit_profile.html',{'form' : form})

@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/change_password.html' , {'form': form})

def contact(request):
    if request.method!='POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        if form.is_valid():
            mail_subject = 'Contact -- By -- ' + form.cleaned_data.get('userName')
            to_email = settings.EMAIL_HOST_USER
            message = form.cleaned_data.get('body')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('home')
    
    context= {'form' : form}
    return render(request, 'music/contact.html', context)


    
def search(request):

    query=request.GET.get('query',None)
   
    blogs=profileModel.objects.all()
    if query is not None:
        blogs=blogs.filter(
        Q(user__username__icontains=query)|
        Q(contactNumber__icontains=query)|
        Q(city__icontains=query)|
        Q(county__icontains=query)|
        Q(country__icontains=query)|
        Q(state__icontains=query)|
        Q(continent__icontains=query)
        

        )
    context={

        'blogs':blogs,
        'query':query
}

    return render(request,'search.html',context)

# def wrist_bandView(request):
#     form= wrist_bandForm()
#     if request.method=='POST':
#         form=wrist_bandForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             return redirect('information')

    
#     context={
#         'form':form,
        
#     }
   
#     return render(request,'music/wrist.html',context)

def InformationView(request):
    form= InformationForm()
    if request.method=='POST':
        form=InformationForm(request.POST )
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
           
            new.save()
            form.save()
            return HttpResponseRedirect(reverse('dashboard', args=[request.user.username])) 

    
    context={
        'form':form,
        
        
    }
   
    return render(request,'music/information.html',context)



def InformationViewEdit(request,id):
    user=request.user
    current_site = get_current_site(request)
    message = render_to_string('music/edit_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'id':id
            })
    mail_subject = 'Activate your account.'
    to_email = request.user.email

    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
    return render(request, 'music/acc_active_email_confirm.html')

def activateinform(request, uidb64, token,id):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        id=id
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
       
        return HttpResponseRedirect(reverse('informationedit1', args=[id])) 
    else:
        return HttpResponse('Activation link is invalid!')

def InformationViewEdit1(request,id):
    obj= Information.objects.get(id=id)
    form= InformationFormEdit(instance=obj )
    if request.method=='POST':
        form=InformationFormEdit(request.POST , instance=obj )
        if form.is_valid():
            new = form.save(commit=False)
            new.user=request.user
            new.first_name_child=obj.first_name_child 
            new.last_name_child=obj.last_name_child
            new.important_information_child=obj.important_information_child
            new.first_name_soc=obj.first_name_soc
            new.last_name_soc=obj.last_name_soc
            new.relation_to_child=obj.relation_to_child
            new.phone_number_soc=obj.phone_number_soc
            new.save()
            form.save()
            return HttpResponseRedirect(reverse('dashboard', args=[request.user.username])) 
    context={
        'form':form,
        
        
    }
   
    return render(request,'music/informationedit.html',context)
