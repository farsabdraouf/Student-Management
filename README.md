# نظام إدارة الطلاب
نظام بسيط لإدارة بيانات الطلاب مبني باستخدام Python و MySQL مع واجهة مستخدم رسومية.

## المتطلبات
- Python 3.7+
- MySQL Server
- المكتبات المطلوبة في ملف requirements.txt

## تنظيم المجلدات

```
student_management/
│
├── config/                 # إعدادات المشروع
│   ├── __init__.py
│   └── database.py        # إعدادات قاعدة البيانات
│
├── models/                 # نماذج البيانات
│   ├── __init__.py
│   └── student.py         # نموذج الطالب
│
├── repositories/          # التعامل مع قاعدة البيانات
│   ├── __init__.py
│   └── student_repository.py
│
├── services/             # منطق الأعمال
│   ├── __init__.py
│   └── student_service.py
│
├── ui/                   # واجهة المستخدم
│   ├── __init__.py
│   └── main_window.py    # النافذة الرئيسية
│
├── utils/                # أدوات مساعدة
│   ├── __init__.py
│   └── validators.py     # التحقق من صحة البيانات
│
├── setup/                # سكربتات الإعداد
│   └── setup_database.py # إعداد قاعدة البيانات
│
├── requirements.txt      # المكتبات المطلوبة
├── main.py              # نقطة البداية
└── README.md            # توثيق المشروع
```

## التثبيت

1. إنشاء البيئة الافتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
venv\Scripts\activate     # على Windows
```

2. قم بتثبيت المكتبات المطلوبة:
```bash
pip install -r requirements.txt
```

3. قم بتعديل إعدادات قاعدة البيانات في ملف config/database.py


4. إعداد قاعدة البيانات:
```bash
python setup/setup_database.py
```

## التشغيل
قم بتشغيل البرنامج باستخدام الأمر:
```bash
python main.py
```

## الميزات
- إضافة طالب جديد
- تحديث بيانات الطالب
- حذف طالب
- البحث في بيانات الطلاب
- عرض جميع الطلاب في جدول