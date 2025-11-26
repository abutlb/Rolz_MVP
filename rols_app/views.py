from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Device, Ticket, TicketComment
from django.db.models import Q
from .forms import TicketForm, TicketCommentForm, DeviceForm

@login_required
def dashboard(request):
    """عرض لوحة التحكم الرئيسية"""
    user = request.user
    
    # للموظفين العاديين: عرض أجهزتهم وتذاكرهم
    if not user.is_staff:
        devices = Device.objects.filter(assigned_to=user)
        tickets = Ticket.objects.filter(created_by=user).order_by('-created_at')
    # لفريق الدعم الفني: عرض جميع التذاكر المفتوحة
    else:
        devices = Device.objects.all()
        tickets = Ticket.objects.exclude(status__in=['RESOLVED', 'CLOSED']).order_by('-priority', '-created_at')
    
    context = {
        'devices': devices,
        'tickets': tickets,
        'new_tickets_count': Ticket.objects.filter(status='NEW').count(),
        'in_progress_tickets_count': Ticket.objects.filter(status='IN_PROGRESS').count(),
        'pending_tickets_count': Ticket.objects.filter(status='PENDING').count(),
    }
    return render(request, 'rols_app/dashboard.html', context)

@login_required
def device_list(request):
    """عرض قائمة الأجهزة"""
    if request.user.is_staff:
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(assigned_to=request.user)
    
    return render(request, 'rols_app/device_list.html', {'devices': devices})

@login_required
def device_detail(request, pk):
    """عرض تفاصيل جهاز محدد"""
    if request.user.is_staff:
        device = get_object_or_404(Device, pk=pk)
    else:
        device = get_object_or_404(Device, pk=pk, assigned_to=request.user)
    
    tickets = device.tickets.all().order_by('-created_at')
    return render(request, 'rols_app/device_detail.html', {'device': device, 'tickets': tickets})

@login_required
def create_device(request):
    """إنشاء جهاز جديد (للمسؤولين فقط)"""
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية للوصول إلى هذه الصفحة')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إنشاء الجهاز بنجاح')
            return redirect('device_list')
    else:
        form = DeviceForm()
    
    return render(request, 'rols_app/device_form.html', {'form': form})

@login_required
def ticket_list(request):
    """عرض قائمة التذاكر"""
    if request.user.is_staff:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    
    return render(request, 'rols_app/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    """إنشاء تذكرة جديدة"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'تم إنشاء التذكرة بنجاح')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        # عرض الأجهزة المخصصة للمستخدم فقط
        if request.user.is_staff:
            form = TicketForm()
        else:
            form = TicketForm()
            form.fields['device'].queryset = Device.objects.filter(assigned_to=request.user)
    
    return render(request, 'rols_app/ticket_form.html', {'form': form})

@login_required
def ticket_detail(request, pk):
    """عرض تفاصيل تذكرة محددة"""
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, pk=pk)
    else:
        # استخدام فلتر لعرض التذاكر التي أنشأها المستخدم أو المعينة له
        user_filter = Q(created_by=request.user) | Q(assigned_to=request.user)
        ticket = get_object_or_404(Ticket.objects.filter(user_filter), pk=pk)
    
    comments = ticket.comments.all().order_by('created_at')
    
    if request.method == 'POST':
        comment_form = TicketCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            messages.success(request, 'تم إضافة التعليق بنجاح')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        comment_form = TicketCommentForm()
    
    context = {
        'ticket': ticket,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'rols_app/ticket_detail.html', context)

@login_required
def update_ticket_status(request, pk):
    """تحديث حالة التذكرة"""
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية للوصول إلى هذه الصفحة')
        return redirect('dashboard')
    
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Ticket.STATUS_CHOICES).keys():
            ticket.status = new_status
            ticket.save()
            messages.success(request, 'تم تحديث حالة التذكرة بنجاح')
        
        # تعيين التذكرة للمستخدم الحالي إذا كانت قيد المعالجة
        if new_status == 'IN_PROGRESS' and not ticket.assigned_to:
            ticket.assigned_to = request.user
            ticket.save()
    
    return redirect('ticket_detail', pk=ticket.pk)