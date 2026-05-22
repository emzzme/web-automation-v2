# XZ Positioner Control UI Starter

Bu klasor, Windows tabanli Python + Qt (PySide6) kontrol arayuzu projesi icin ICD-oncesi tam demo altyapisidir.

## Hedef
- Komuta kontrol bilgisayarinda calisan masaustu uygulama
- XZ lineer pozisyoner sistemi kontrolu
- VNA (S21) canli izleme, tarama haritasi, zaman serisi
- Operator odakli, endustriyel, stabil arayuz

## Hızlı Baslangic
1. `scripts/setup_dev_env.bat`
2. UI tasarim: `scripts/open_qt_designer.bat`
3. Canli UI onizleme: `scripts/run_ui_live_preview.bat`
4. Tam fonksiyonlu demo: `scripts/launch_demo_full.bat`
5. Testler: `scripts/run_tests.bat`

## Qt UI + Gelistirme Dokumani
Adim adim rehber:
- `docs/qt_designer_gelistirme_rehberi_tr.md`

## Klasor Yapisi
- `src/xz_control_ui/main.py`: Ana uygulama (is kurallari + widget baglantilari)
- `src/xz_control_ui/ui/main_window.ui`: Qt Designer ana arayuz
- `src/xz_control_ui/ui/theme.qss`: QSS tema
- `src/xz_control_ui/services/`: Mock ve runtime servisleri
- `src/xz_control_ui/icd/`: ICD parse ve aktivasyon katmani
- `config/system_requirements.yaml`: Teknik isterlerin makine-okunur kaydi
- `config/activation.json`: Runtime baglanti aktivasyon dosyasi
- `docs/qt_designer_gelistirme_rehberi_tr.md`: UI gelistirme adimlari

## Not
Bu surum, donanimsiz ortamda calisan demo/prototiptir. Gercek cihaz entegrasyonu adapter yapisi uzerinden ilerler.

## VS Code Ile Demo Gosterimi
1. VS Code ile proje klasorunu acin.
2. Terminalde `scripts/setup_dev_env.bat` calistirin.
3. Tam ozellikli (hareketli kutucuklar + sag tik panel secimi) demo icin:
   - `scripts/launch_demo_full.bat`
   - Bu script `XZ_UI_MODE=legacy` ile acilir ve tum gelistirdigimiz panel/dock ozelliklerini korur.
4. Sadece Qt tasarim onizleme icin:
   - `scripts/run_ui_live_preview.bat`
   - Bu modda islevlerin bir kismi olmayabilir; amac tasarimdir.

## Script Notlari
- `scripts/run_tests.bat` artik CI-uyumludur; test bitince `pause` yapmaz ve cikis kodunu dogru dondurur.
- `scripts/run_ui_live_preview.bat` artik tam demo arayuzunu acarak (tum fonksiyonlar gorunur) tema (`theme.qss`) degisikliklerini canli uygular.

## ICD Giris Taslagi (Kullaniciya Verilecek Format)
- Ana rehber: `docs/ICD_PROGRAM_INPUT_GUIDE_TR.md`
- Hazir taslak dosyalar: `config/icd_template/`
  - `icd_runtime_template.json`
  - `activation.json`
  - `command_map.json`
  - `ttl_io_map.json`

Hizli kullanim:
1. `config/icd_template/icd_runtime_template.json` doldur
2. `runtime_activation` bolumunu `config/activation.json` dosyasina kopyala
3. Uygulamayi yeniden baslat (`scripts/launch_demo_full.bat`)

## Yeni Bilgisayarda Tek Tik Baslangic
- `ONE_CLICK_SETUP.bat` dosyasini calistir.
- Ortam kurulur, testler calisir, demo acilir.
- Devam notlari: `docs/CONTINUE_FROM_HERE_TR.md`
