from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import CustomSignupForm, CustomLoginForm
from .models import UserProfile
from .models import Ticket



def login_view(request):
    form = CustomLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    role = user.userprofile.role
                    if role == 'Admin':
                        return redirect('admin_dashboard')
                    elif role == 'Agent':
                        return redirect('agent_dashboard')
                    else:
                        return redirect('customer_dashboard')
                else:
                    form.add_error(None, "Invalid email or password")
            except User.DoesNotExist:
                form.add_error('email', "No user registered with this email")
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    form = CustomSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            role = form.cleaned_data['role']

            # ✅ Check if role is Admin or Agent and already exists
            if role in ['Admin', 'Agent'] and UserProfile.objects.filter(role=role).exists():
                form.add_error('role', f"{role} account already exists. Only one signup allowed.")
            
            elif password1 != password2:
                form.add_error('password2', "Passwords do not match")
            elif User.objects.filter(email=email).exists():
                form.add_error('email', "Email is already registered")
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password1,
                    first_name=name
                )

                UserProfile.objects.create(user=user, role=role)

                return redirect('login')
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def submit_ticket(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        Ticket.objects.create(
            customer=request.user,
            subject=subject,
            description=description,
            status='Open'  # ✅ Optional, because it's default
        )

        return redirect('customer_dashboard')
 # or wherever you want to show confirmation


def open_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, status='Open').order_by('id')
    print("Logged in user:", request.user)
    print("Tickets fetched:", tickets)
    print("Found Open Tickets:", tickets)  # <-- Debug
    return render(request, 'accounts/open_tickets.html', {'tickets': tickets})

from django.shortcuts import get_object_or_404

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, customer=request.user)
    return render(request, 'accounts/ticket_detail.html', {'ticket': ticket})


from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_ticket(request, ticket_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        description = data.get('description')
        try:
            ticket = Ticket.objects.get(id=ticket_id, customer=request.user)
            ticket.subject = subject
            ticket.description = description
            ticket.save()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found'})

@csrf_exempt
def delete_ticket(request, ticket_id):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(id=ticket_id, customer=request.user)
            ticket.delete()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found'})





from django.http import HttpResponse

def admin_dashboard(request):
    return HttpResponse("Welcome to Admin Dashboard!")

def agent_dashboard(request):
    return HttpResponse("Welcome to Agent Dashboard!")

def customer_dashboard(request):
    user = request.user
    open_count = Ticket.objects.filter(customer=user, status='Open').count()
    
    # Sort by -id to get recent tickets first
    my_tickets = Ticket.objects.filter(customer=user).order_by('-id')

    return render(request, 'accounts/customer_dashboard.html', {
        'open_count': open_count,
        'my_tickets': my_tickets
    })

    return render(request, 'accounts/customer_dashboard.html', {
        'open_count': open_count,
    })
