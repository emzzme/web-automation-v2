# Mimari (TR)

## 1) Katmanlar
- UI Katmani (`ui/`): PySide6 widget'lari, grafik panelleri, operator akisi
- Uygulama Servisleri (`services/`): Pozisyoner, VNA, TTL IO adaptorleri
- Core Katmani (`core/`): Konfig, durum modelleri, emniyet kurallari
- Data Katmani (`data/` gelecekte): Kalici log, recete, olcum dosyalari

## 2) Donanim Adapter Stratejisi
Her cihaz icin interface + implementation:
- `IPositionerDriver` -> `MockPositionerDriver`, `SerialPositionerDriver`
- `IVnaDriver` -> `MockVnaDriver`, `ScpiVnaDriver`
- `ITtlDriver` -> `MockTtlDriver`, `UsbDioTtlDriver`

UI yalnizca interface'lerle konusur. Boylese:
- Donanim yokken mock ile gelistirme
- Sahada gercek surucuye gecis kolayligi
- Test kapsami artisi

## 3) Guvenlik ve Emniyet
- Soft-limit: X/Z eksen min/max disina cikma engeli
- Hata durumunda otomatik STOP
- Komut kuyrugu timeout / retry
- E-stop input destek noktasi
- Log seviyesi: INFO/WARN/ERROR + olay kodu

## 4) Performans Hedefleri
- UI yenileme: 5-10 Hz
- Telemetri: en az 2 Hz stabil
- Tarama ilerleme update: <= 300 ms gecikme

## 5) Dosya ve Oturum Yonetimi
- Proje bazli kayit dizini
- Recete json/yaml
- Olcum export: CSV + ham binary + metadata json

## 6) Test Stratejisi
- Unit test: limit kontrol, komut parser, recete validasyon
- Integration test: mock driver ile tarama akisi
- Soak test: 8 saat simule telemetri

## 7) Teknoloji
- Python 3.11+
- PySide6
- pyqtgraph
- pydantic (onerilir)
- pyserial (gercek cihaz baglantisinda)
