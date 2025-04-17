

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomSignupForm, CustomLoginForm, CreateAgentForm
from .models import UserProfile, Ticket

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
            role = form.cleaned_data['role']

            # Optionally, allow only one Admin or Agent account (if needed)
            if role in ['Admin', 'Agent'] and UserProfile.objects.filter(role=role).exists():
                form.add_error('role', f"{role} account already exists. Only one signup allowed.")
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


def admin_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in as an admin.")
        return redirect('login')
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'Admin':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    # Retrieve all agents (users whose role is Agent)
    agents = User.objects.filter(userprofile__role='Agent')
    return render(request, 'accounts/admin_dashboard.html', {'agents': agents})


def agent_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in as an agent.")
        return redirect('login')
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'Agent':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    # Render a simplified agent dashboard.
    return render(request, 'accounts/agent_dashboard.html')


def agent_tickets(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in as an agent.")
        return redirect('login')
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'Agent':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    tickets = Ticket.objects.filter(agents=request.user)
    context = {
        'tickets': tickets,
    }
    return render(request, 'accounts/agent_tickets.html', context)


def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


def create_agent(request):
    """
    Displays a form to create an agent.
    After creation, the agent can later log in and view their dashboard.
    """
    form = CreateAgentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            # Create the agent user.
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=name
            )
            UserProfile.objects.create(user=user, role='Agent')
            messages.success(request, "Agent created successfully.")
            return redirect('admin_dashboard')
    return render(request, 'accounts/create_agent.html', {'form': form})


def assign_ticket(request, agent_id):
    """
    Displays a dummy list of tickets as checkboxes so the admin can assign tickets to the agent.
    After selecting and clicking "Finish," the selected tickets are assigned and the view redirects
    back to the admin dashboard.
    """
    # Restrict access to admin only.
    if not request.user.is_authenticated or request.user.userprofile.role != 'Admin':
        messages.error(request, "Only admins can assign tickets.")
        return redirect('login')

    agent = get_object_or_404(User, id=agent_id)
    
    # Create dummy tickets if none exist.
    if Ticket.objects.count() == 0:
        Ticket.objects.bulk_create([
            Ticket(title="Ticket 1"),
            Ticket(title="Ticket 2"),
            Ticket(title="Ticket 3")
        ])
    dummy_tickets = Ticket.objects.all()

    if request.method == 'POST':
        selected_ticket_ids = request.POST.getlist('tickets')
        if selected_ticket_ids:
            selected_tickets = Ticket.objects.filter(id__in=selected_ticket_ids)
            for ticket in selected_tickets:
                ticket.agents.add(agent)
            messages.success(request, "Tickets assigned successfully!")
        # Redirect back to the admin dashboard.
        return redirect('admin_dashboard')

    context = {
        'agent': agent,
        'dummy_tickets': dummy_tickets,
    }
    return render(request, 'accounts/assign_ticket.html', context)


def delete_agent(request, agent_id):
    """
    Deletes the specified agent and then redirects to the admin dashboard.
    """
    agent = get_object_or_404(User, id=agent_id)
    agent.delete()
    messages.success(request, "Agent deleted successfully.")
    return redirect('admin_dashboard')
