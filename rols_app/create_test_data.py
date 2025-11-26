import os
import sys
import django
import random
from datetime import datetime, timedelta

# إعداد بيئة Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_rols.settings')
django.setup()

# استيراد النماذج بعد إعداد البيئة
from django.contrib.auth.models import User
from rols_app.models import Device, Ticket, TicketComment
from django.utils import timezone

def create_test_data():
    print("بدء إنشاء البيانات التجريبية...")
    
    # إنشاء المستخدمين
    users = []
    # إنشاء مستخدم مسؤول إذا لم يكن موجودًا
    try:
        admin_user = User.objects.get(username='admin')
        print("المستخدم المسؤول موجود بالفعل")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("تم إنشاء المستخدم المسؤول: admin / admin123")
    
    users.append(admin_user)
    
    # إنشاء مستخدمين عاديين
    for i in range(1, 10):
        username = f'user{i}'
        email = f'user{i}@example.com'
        password = f'password{i}'
        
        try:
            user = User.objects.get(username=username)
            print(f"المستخدم {username} موجود بالفعل")
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password)
            print(f"تم إنشاء المستخدم: {username} / {password}")
        
        users.append(user)
    
    # إنشاء فريق الدعم الفني (مستخدمين لديهم صلاحيات إدارية)
    for i in range(1, 4):
        username = f'support{i}'
        email = f'support{i}@example.com'
        password = f'support{i}123'
        
        try:
            user = User.objects.get(username=username)
            print(f"مستخدم الدعم الفني {username} موجود بالفعل")
            user.is_staff = True
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)
            print(f"تم إنشاء مستخدم الدعم الفني: {username} / {password}")
        
        users.append(user)
    
    # إنشاء الأجهزة
    device_types = ['LAPTOP', 'DESKTOP', 'PRINTER', 'SCANNER', 'OTHER']
    laptop_models = ['Dell XPS 15', 'HP EliteBook', 'Lenovo ThinkPad', 'MacBook Pro', 'Asus ZenBook']
    desktop_models = ['Dell OptiPlex', 'HP Pavilion', 'Lenovo ThinkCentre', 'iMac', 'Asus ROG']
    printer_models = ['HP LaserJet', 'Canon PIXMA', 'Epson EcoTank', 'Brother MFC', 'Xerox WorkCentre']
    scanner_models = ['Epson Perfection', 'Canon CanoScan', 'HP ScanJet', 'Brother ADS', 'Fujitsu ScanSnap']
    other_models = ['Projector Epson', 'Monitor Dell', 'Keyboard Logitech', 'Mouse Microsoft', 'Headset Jabra']
    
    devices = []
    
    for i in range(1, 101):
        device_type = random.choice(device_types)
        
        if device_type == 'LAPTOP':
            model = random.choice(laptop_models)
        elif device_type == 'DESKTOP':
            model = random.choice(desktop_models)
        elif device_type == 'PRINTER':
            model = random.choice(printer_models)
        elif device_type == 'SCANNER':
            model = random.choice(scanner_models)
        else:
            model = random.choice(other_models)
        
        serial_number = f'SN-{device_type[:3]}-{random.randint(100000, 999999)}'
        
        # تخصيص 80% من الأجهزة للمستخدمين
        if random.random() < 0.8:
            assigned_to = random.choice(users[:9])  # فقط المستخدمون العاديون (بدون المسؤولين وفريق الدعم)
            date_assigned = timezone.now() - timedelta(days=random.randint(1, 365))
        else:
            assigned_to = None
            date_assigned = None
        
        try:
            device = Device.objects.get(serial_number=serial_number)
            print(f"الجهاز برقم تسلسلي {serial_number} موجود بالفعل")
        except Device.DoesNotExist:
            device = Device.objects.create(
                serial_number=serial_number,
                device_type=device_type,
                model=model,
                assigned_to=assigned_to,
                date_assigned=date_assigned,
                notes=f"هذا جهاز تجريبي رقم {i}"
            )
            print(f"تم إنشاء جهاز: {device_type} - {model} ({serial_number})")
        
        devices.append(device)
    
    # إنشاء التذاكر
    ticket_titles = [
        "الجهاز لا يعمل",
        "مشكلة في الطباعة",
        "الشاشة لا تعمل",
        "برنامج Office لا يعمل",
        "مشكلة في الاتصال بالإنترنت",
        "البريد الإلكتروني لا يعمل",
        "الجهاز بطيء جدًا",
        "مشكلة في تسجيل الدخول",
        "تثبيت برنامج جديد",
        "استعادة ملفات محذوفة",
        "تحديث نظام التشغيل",
        "مشكلة في الصوت",
        "الماسح الضوئي لا يعمل",
        "تهيئة جهاز جديد",
        "نقل البيانات إلى جهاز جديد"
    ]
    
    ticket_descriptions = [
        "الجهاز لا يعمل عند الضغط على زر التشغيل.",
        "لا يمكنني الطباعة من الجهاز، تظهر رسالة خطأ.",
        "الشاشة سوداء ولكن الجهاز يعمل.",
        "برنامج Office يتوقف عن العمل عند فتح ملف.",
        "لا يمكنني الاتصال بالإنترنت رغم أن الشبكة متصلة.",
        "لا يمكنني استلام أو إرسال رسائل البريد الإلكتروني.",
        "الجهاز بطيء جدًا عند تشغيل أي برنامج.",
        "نسيت كلمة المرور ولا يمكنني تسجيل الدخول.",
        "أحتاج إلى تثبيت برنامج جديد للعمل.",
        "قمت بحذف ملفات مهمة بالخطأ وأحتاج إلى استعادتها.",
        "أحتاج إلى تحديث نظام التشغيل إلى أحدث إصدار.",
        "لا يوجد صوت في الجهاز رغم أن مستوى الصوت مرتفع.",
        "الماسح الضوئي لا يتعرف على المستندات.",
        "استلمت جهازًا جديدًا وأحتاج إلى تهيئته للعمل.",
        "أحتاج إلى نقل بياناتي من الجهاز القديم إلى الجهاز الجديد."
    ]
    
    # إنشاء 50 تذكرة
    for i in range(1, 51):
        # اختيار جهاز مخصص لمستخدم
        assigned_devices = [d for d in devices if d.assigned_to is not None]
        if not assigned_devices:
            continue
        
        device = random.choice(assigned_devices)
        user = device.assigned_to
        
        title_index = random.randint(0, len(ticket_titles) - 1)
        title = ticket_titles[title_index]
        description = ticket_descriptions[title_index]
        
        # تحديد حالة التذكرة
        status_choices = ['NEW', 'IN_PROGRESS', 'PENDING', 'RESOLVED', 'CLOSED']
        status_weights = [0.2, 0.3, 0.2, 0.2, 0.1]  # احتمالية كل حالة
        status = random.choices(status_choices, weights=status_weights, k=1)[0]
        
        # تحديد الأولوية
        priority_choices = ['LOW', 'MEDIUM', 'HIGH', 'URGENT']
        priority_weights = [0.3, 0.4, 0.2, 0.1]  # احتمالية كل أولوية
        priority = random.choices(priority_choices, weights=priority_weights, k=1)[0]
        
        # تحديد تاريخ الإنشاء
        created_at = timezone.now() - timedelta(days=random.randint(1, 30))
        
        # تحديد المسؤول عن التذكرة (إذا كانت قيد المعالجة أو أعلى)
        if status in ['IN_PROGRESS', 'PENDING', 'RESOLVED', 'CLOSED']:
            assigned_to = random.choice(users[10:])  # فريق الدعم الفني
            resolution = "تم حل المشكلة بنجاح." if status in ['RESOLVED', 'CLOSED'] else ""
        else:
            assigned_to = None
            resolution = ""
        
        ticket = Ticket.objects.create(
            title=f"{title} - تذكرة {i}",
            description=description,
            created_by=user,
            device=device,
            status=status,
            priority=priority,
            created_at=created_at,
            assigned_to=assigned_to,
            resolution=resolution
        )
        
        print(f"تم إنشاء تذكرة: {ticket.title} ({ticket.get_status_display()})")
        
        # إضافة تعليقات على التذاكر
        if random.random() < 0.7:  # 70% من التذاكر لها تعليقات
            num_comments = random.randint(1, 5)
            
            for j in range(num_comments):
                comment_user = user if j % 2 == 0 else (assigned_to if assigned_to else random.choice(users[10:]))
                comment_text = random.choice([
                    "هل يمكن توضيح المشكلة أكثر؟",
                    "سأقوم بفحص المشكلة في أقرب وقت.",
                    "هل يمكن إعادة تشغيل الجهاز ومحاولة مرة أخرى؟",
                    "المشكلة معقدة وتحتاج إلى وقت أطول للحل.",
                    "تم حل المشكلة، يرجى التأكد من أن كل شيء يعمل الآن.",
                    "هل هناك أي تحديثات حول المشكلة؟",
                    "سأقوم بزيارتك غدًا لفحص الجهاز.",
                    "يرجى تزويدي برقم مكتبك."
                ])
                
                comment_date = ticket.created_at + timedelta(hours=random.randint(1, 48))
                if comment_date > timezone.now():
                    comment_date = timezone.now()
                
                TicketComment.objects.create(
                    ticket=ticket,
                    user=comment_user,
                    comment=comment_text,
                    created_at=comment_date
                )
                
                print(f"  تم إضافة تعليق على التذكرة {ticket.id} بواسطة {comment_user.username}")
    
    print("تم الانتهاء من إنشاء البيانات التجريبية بنجاح!")
    print("\nبيانات تسجيل الدخول:")
    print("المسؤول: admin / admin123")
    print("المستخدمون العاديون: user1 إلى user9 / password1 إلى password9")
    print("فريق الدعم الفني: support1 إلى support3 / support1123 إلى support3123")

if __name__ == '__main__':
    create_test_data()