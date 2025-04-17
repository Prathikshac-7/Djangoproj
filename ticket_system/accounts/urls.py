from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('agent-dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('submit-ticket/', views.submit_ticket, name='submit_ticket'),
    path('open-tickets/', views.open_tickets, name='open_tickets'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('tickets/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
]
