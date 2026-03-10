[app]
# (str) اسم التطبيق الذي سيظهر على الهاتف
title = Architect Mobile v12

# (str) اسم الحزمة (لا تستخدم فراغات)
package.name = architect_mobile

# (str) النطاق البرمجي
package.domain = com.architect.v12

# (str) مسار ملف الكود الرئيسي
source.dir = .

# (list) ملفات المصدر التي سيتم تضمينها
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) نسخة التطبيق
version = 12.0

# (list) المكتبات المطلوبة (تم ضبطها لتشمل محركات التشفير والشبكة)
requirements = python3,kivy,aiohttp,aiofiles,certifi,idna,charset-normalizer,multidict,yarl,attrs

# (str) مسار الأيقونة (تأكد من وجود ملف icon.png في المستودع)
icon.filename = %(source.dir)s/icon.png

# (str) مسار شاشة البداية (تأكد من وجود ملف splash.png في المستودع)
presplash.filename = %(source.dir)s/splash.png

# (list) التصاريح (صلاحية الإنترنت ضرورية جداً للهجوم)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) المستوى الأدنى للأندرويد (API 21 تعني أندرويد 5.0 فما فوق)
android.minapi = 21

# (int) المستوى المستهدف (API 33 لأحدث توافق مع متجر جوجل)
android.sdk = 33

# (str) اتجاه الشاشة (Portrait = طولي)
orientation = portrait

# (bool) لجعل التطبيق يعمل بملء الشاشة
fullscreen = 1

# (list) المعماريات التي سيدعمها التطبيق (arm64 للأجهزة الحديثة)
android.archs = arm64-v8a, armeabi-v7a

# (bool) تفعيل هذه الميزة يسمح للتطبيق بالعمل في الخلفية
android.allow_backup = True

[buildozer]
# (int) مستوى التنبيهات (2 يعني عرض الأخطاء بوضوح)
log_level = 2

# (int) حذف ملفات البناء القديمة لتجنب المشاكل
warn_on_root = 1
