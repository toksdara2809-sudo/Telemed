from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    # Redirect back to where user came from, or dashboard home
    next_url = request.GET.get('next', 'dashboard_home')
    return redirect(next_url)

@login_required
def mark_all_notifications_as_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    next_url = request.GET.get('next', 'dashboard_home')
    return redirect(next_url)
