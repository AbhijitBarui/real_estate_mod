from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from contacts.models import Contact

def register(request):
    if request.method == "POST":
        #register suer logic
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #password match check
        if password == password2:
            #check username:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else:
                #check email:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'that email is already registered with us')
                    return redirect('login')
                else:
                    #looks good
                    user = User.objects.create_user(
                        username =username,
                        password = password,
                        email = email,
                        first_name = first_name,
                        last_name = last_name,
                    )
                    #login after register:
                    auth.login(request, user)
                    messages.success(request, 'you are now logged in')
                    return redirect('index')
                    #manual login:
                    #user.save()
                    #messages.success(request, 'you are now registered, please proceed to log in)
                    #return redirect('login)
        else:
            messages.error(request, 'passwords do not match')
        return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        #login suer logic
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
        return
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)
