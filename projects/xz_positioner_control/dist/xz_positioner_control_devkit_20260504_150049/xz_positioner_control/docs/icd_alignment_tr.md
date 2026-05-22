# Dokuman Uyum Ozeti (210426)

Bu proje iskeleti, `Near_Field_Antenna_Test_Blok_Diyagram ve Satin Alma Tablosu_210426.docx` icerigindeki blok yapiya uygun olarak kurgulandi.

## Diyagram Katman Eslesmesi
1. Guc Altyapisi (220VAC, UPS, koruma)
2. Kontrol Bilgisayari ve Otomasyon Kati (GUI, recete, log, DLL/API)
3. Pozisyoner Kontrol Unitesi (X/Z senkron hareket, hiz/ivme, alarm)
4. RF Olcum Cihazi - VNA (LAN/USB/SCPI, tetik senkron)
5. Hareket Kati - XZ Pozisyoner (motor suruculer, encoder geri besleme)
6. TTL Trigger / Digital I/O (step trigger cikisi, durum/konum aktarimi)
7. Acil Stop / Home / Limit Sensor zinciri

## Verilen Teknik Isterlerin Kod Yansimasi
- 4m x 3m aktif tarama alani ve 0.60m derinlik limiti `config/system_requirements.yaml` icinde.
- Soft-limit, home/limit, estop zorunlulugu mimari seviyede ayrildi.
- Konum/hassasiyet hedefleri kabul kriteri olarak modele eklendi.
- USB/Ethernet + SCPI + TTL interfaceleri ICD placeholder olarak ayrildi.

## ICD Geldiginde Aktivasyon
1. ICD dokumanini sisteme ver.
2. `scripts/resumable_pipeline.py --icd <dosya>` ile parse et.
3. `config/activation.json` alanlarini ICD'ye gore doldur.
4. Runtime tarafi `state/active_connections.json` uretir.

## Kabul Testine Hazirlik
- Lazer tracker ile konum dogrulama gereksinimi dokumanlandi.
- Dogrulama raporu icin ham veri + metadata kayit akisi planlandi.
