# Qt Designer Gelistirme Rehberi (Adim Adim)

Bu dokuman, projeyi Qt Designer uzerinden nasil guncelleyeceginizi ve degisiklikleri calisan uygulamaya nasil yansitacaginizi anlatir.

## 1) Ilk Kurulum
1. Proje klasorunde `scripts/setup_dev_env.bat` calistirin.
2. Kurulum bitince `.venv` ve tum bagimliliklar hazir olur.

## 2) Tasarimi Qt Designer ile Acma
1. `scripts/open_qt_designer.bat` calistirin.
2. Acilan dosya: `src/xz_control_ui/ui/main_window.ui`
3. Sol panel (Widget Box) ve Object Inspector ile yerlesimi duzenleyin.

## 3) Hangi Dosya Ne Ise Yarar?
- `src/xz_control_ui/ui/main_window.ui`: Ana tasarim (Designer dosyasi)
- `src/xz_control_ui/ui/theme.qss`: Renk/font/stil
- `src/xz_control_ui/main.py`: Is kurallari, sinyal baglantilari, grafik ve tarama fonksiyonlari

## 4) Degisiklikleri Aninda Gormek
1. Bir terminalde `scripts/run_ui_live_preview.bat` calistirin.
2. Designer'da `main_window.ui` kaydedin.
3. Onizleme penceresi otomatik yenilenir.

Not: Bu mod hizli UI onizlemesi icindir.

## 5) Tam Fonksiyonlu Uygulamada Test
1. `scripts/launch_demo_full.bat` calistirin.
2. Tarama, rapor, VNA paneli, log gibi tum akislari test edin.
3. Gerekirse `scripts/run_tests.bat` ile otomatik testleri kosun.

## 6) Sinyal/Widget Baglantisi Kurallari
Yeni bir buton veya alan eklerken:
1. Designer'da `objectName` verin (ornek: `newActionButton`).
2. `main.py` icinde `findChild(...)` ile widget'i alin.
3. Islev baglayin: `button.clicked.connect(self.your_handler)`
4. Handler fonksiyonunu ekleyin.

## 7) Guvenli Gelistirme Akisi
1. UI degisikligi yap
2. Live preview ile kontrol et
3. Full demo ile fonksiyon testi yap
4. `run_tests.bat` calistir
5. Paketlemeden once rapor akisini test et

## 8) Sik Hatalar
- `pyside6-designer bulunamadi`: once `setup_dev_env.bat`
- Degisiklik gorunmuyor: dogru dosya `main_window.ui` kaydedildi mi kontrol et
- Fonksiyon calismiyor: `main.py` icinde ilgili `objectName` baglandi mi kontrol et

## 9) Dagitim Oncesi Kontrol Listesi
- UI yerlesimleri responsive mi?
- Buton metinleri okunuyor mu?
- Tarama bitis popup'i ve rapor olusumu calisiyor mu?
- `Raporu Indir` durumu (gri/yesil) dogru mu?
- Otomatik rapor `state/reports` altina dusuyor mu?
