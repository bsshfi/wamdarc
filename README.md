# wamdarc.com — النسخة الثالثة (عربي + إنجليزي، نموذج تواصل، وبطاقات سهم وفلق وخُطى)

## طريقة التحديث على GitHub
ارفع **محتويات** هذا المجلد على نفس المستودع واستبدل الموجود:
- `index.html` و`thanks.html` (صفحة الشكر بعد الإرسال — جديدة)
- مجلد `assets/` كامل (فيه `assets/sahm/` و`assets/falaq/` و`assets/khuta/` للأيقونات والصور)
- `CNAME` (لا تحذفه)

## تفعيل نموذج التواصل (مرة وحدة فقط)
النموذج يرسل عن طريق خدمة FormSubmit المجانية إلى contact@wamdarc.com
(واللي يتحوّل لـ Gmail حقك عن طريق Email Forwarding في Spaceship).
1. تأكد إن `contact` مضاف في Email Forwarding في Spaceship.
2. افتح wamdarc.com وأرسل رسالة تجربة من النموذج.
3. بيوصلك إيميل من FormSubmit فيه زر **Activate Form** — اضغطه.
4. من بعدها كل رسالة توصلك مباشرة.

(اختياري) بعد التفعيل يعطيك FormSubmit رابط سري بدل الإيميل، ضعه مكان
`https://formsubmit.co/contact@wamdarc.com` داخل index.html عشان يخفي إيميلك عن البوتات.

## الحماية من السبام
- سؤال تحقق حسابي يتغيّر كل مرة
- حقل مخفي يصيد البوتات
- صفحة «أنا لست روبوت» من FormSubmit بعد الإرسال

## اللغة
زر EN / عربي في الأعلى، والموقع يتذكر اختيار الزائر.
روابط مباشرة: wamdarc.com/?lang=en و wamdarc.com/?lang=ar

## بطاقات التطبيقات
في قسم «منتجاتنا» كل بطاقة رابط كامل يفتح التطبيق في تبويب جديد:
- سهم: https://sahm.wamdarc.com — الصور في `assets/sahm/` (main / list / qibla .webp)
- فلق: https://falaq.wamdarc.com — الصور في `assets/falaq/` (prayer / azkar / moon .webp)
- خُطى: https://khuta.wamdarc.com — الصور في `assets/khuta/` (map / trips / passport .webp)
لتغيير أي صورة استبدلها بنفس الاسم.
