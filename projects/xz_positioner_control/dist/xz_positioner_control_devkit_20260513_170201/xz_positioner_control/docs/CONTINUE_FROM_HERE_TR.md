# Kaldigimiz Yerden Devam (Yeni Bilgisayar)

## Tek Tik Kurulum
- Proje klasorunde `ONE_CLICK_SETUP.bat` calistir.
- Bu dosya otomatik olarak:
  1) Python ortamini kurar
  2) Testleri calistirir
  3) Demo uygulamayi açar

## Manuel Komutlar
- Ortam kurulum: `scripts/setup_dev_env.bat`
- Tam demo: `scripts/launch_demo_full.bat`
- UI preview: `scripts/run_ui_live_preview.bat`
- Testler: `scripts/run_tests.bat`
- Qt Designer: `scripts/open_qt_designer.bat`

## Projenin Son Durumu (Bu Paket)
- UI mode + dock panel sistemi aktif
- Ust bar butonlari bagli ve test edildi
- Sag tik panel ac/kapa aktif
- Tarama, rapor, VNA panel akisi aktif
- ICD template ve kullanim rehberi mevcut

## Claude/Codex ile Devam Promptu
Asagidaki metni yeni oturumda ilk mesaj olarak ver:

"""
Bu projede kaldigimiz yerden devam et.
Once durumu ozetle ve su alanlari dogrula:
1) Ust bar butonlari (VNA, Ayarlar, Tam Ekran, Dry-Run)
2) Dock tasima + sag tik panel ac/kapa
3) Tarama popup + rapor olusumu
4) ICD template akisi
Sonra kalan UI iyilestirmelerini uygula.
Her adim sonunda degisen dosyalar + test komutlari + sonuc yaz.
"""
