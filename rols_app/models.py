from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    """نموذج لتخزين معلومات الأجهزة"""
    DEVICE_TYPES = [
        ('LAPTOP', 'لابتوب'),
        ('DESKTOP', 'كمبيوتر مكتبي'),
        ('PRINTER', 'طابعة'),
        ('SCANNER', 'ماسح ضوئي'),
        ('OTHER', 'أخرى'),
    ]
    
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="الرقم التسلسلي")
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES, verbose_name="نوع الجهاز")
    model = models.CharField(max_length=100, verbose_name="موديل الجهاز")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices", verbose_name="مخصص للموظف")
    date_assigned = models.DateField(null=True, blank=True, verbose_name="تاريخ التخصيص")
    notes = models.TextField(blank=True, verbose_name="ملاحظات")
    
    def __str__(self):
        return f"{self.get_device_type_display()} - {self.model} ({self.serial_number})"
    
    class Meta:
        verbose_name = "جهاز"
        verbose_name_plural = "الأجهزة"

class Ticket(models.Model):
    """نموذج لتخزين تذاكر الدعم الفني"""
    STATUS_CHOICES = [
        ('NEW', 'جديدة'),
        ('IN_PROGRESS', 'قيد المعالجة'),
        ('PENDING', 'معلقة'),
        ('RESOLVED', 'تم الحل'),
        ('CLOSED', 'مغلقة'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'منخفضة'),
        ('MEDIUM', 'متوسطة'),
        ('HIGH', 'عالية'),
        ('URGENT', 'عاجلة'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="عنوان المشكلة")
    description = models.TextField(verbose_name="وصف المشكلة")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_tickets", verbose_name="مقدم الطلب")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="tickets", verbose_name="الجهاز المتأثر")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="حالة التذكرة")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name="الأولوية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets", verbose_name="معين إلى")
    resolution = models.TextField(blank=True, verbose_name="الحل")
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "تذكرة"
        verbose_name_plural = "التذاكر"

class TicketComment(models.Model):
    """نموذج لتخزين التعليقات على التذاكر"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments", verbose_name="التذكرة")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    comment = models.TextField(verbose_name="التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    def __str__(self):
        return f"تعليق على {self.ticket.title} بواسطة {self.user.username}"
    
    class Meta:
        verbose_name = "تعليق"
        verbose_name_plural = "التعليقات"