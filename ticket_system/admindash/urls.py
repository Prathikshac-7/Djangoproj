from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent-tickets/', views.agent_tickets, name='agent_tickets'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    # Create Agent page
    path('create-agent/', views.create_agent, name='create_agent'),
    # Ticket assignment and agent deletion
    path('agent/<int:agent_id>/assign/', views.assign_ticket, name='assign_ticket'),
    path('agent/delete/<int:agent_id>/', views.delete_agent, name='delete_agent'),
]
