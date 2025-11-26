import datetime

def current_year(request):
    """إضافة السنة الحالية إلى سياق القوالب"""
    return {
        'current_year': datetime.datetime.now().year
    }