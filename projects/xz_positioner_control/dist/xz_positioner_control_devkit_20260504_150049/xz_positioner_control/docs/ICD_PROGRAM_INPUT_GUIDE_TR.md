# ICD Teslim Formati ve Programa Verme Rehberi

Bu rehber, gelecek ICD bilgilerini elle doldurup programa sorunsuz vermeniz icin hazirlandi.

## 1) Kullanilacak Dosyalar
Klasor: `config/icd_template/`

- `icd_runtime_template.json`:
  Tum teknik alanlari iceren ana taslak (dokumantasyon + entegrasyon)
- `activation.json`:
  Programin su an runtime'da aktif olarak kullandigi kritik baglanti dosyasi
- `command_map.json`:
  Controller komut eslemeleri
- `ttl_io_map.json`:
  TTL pin eslemeleri

## 2) Programin Zorunlu Olarak Bekledigi Alanlar
Su an uygulama dogrudan `config/activation.json` dosyasini okur ve asagidaki 5 alan zorunludur:

```json
{
  "controller_transport": "USB | LAN",
  "controller_target": "COM5 | 10.0.21.50:5025",
  "vna_transport": "LAN | USB",
  "vna_target": "10.0.21.151 | VISA_RESOURCE",
  "trigger_mode": "TTL_STEP | MANUAL"
}
```

## 3) Adim Adim Doldurma ve Uygulama
1. `config/icd_template/icd_runtime_template.json` dosyasini acin.
2. ICD dokumanindan gelen gercek cihaz bilgilerini tum alanlara yazin.
3. Bu ana dosyadan `runtime_activation` bolumunu alin.
4. `config/activation.json` dosyasina yapistirin ve kaydedin.
5. Uygulamayi yeniden baslatin (`scripts/launch_demo_full.bat`).

## 4) Ornek Canli Kullanima Alma
- USB controller ve LAN VNA icin:
  - `controller_transport`: `USB`
  - `controller_target`: `COM5`
  - `vna_transport`: `LAN`
  - `vna_target`: `10.0.21.151`
  - `trigger_mode`: `TTL_STEP`

## 5) Dogrulama Kontrol Listesi
- Runtime satirinda beklenen mod gorunuyor mu?
- VNA baglanti paneli acilip ayarlar uygulanabiliyor mu?
- Tarama baslat/duraklat/devam/islemleri calisiyor mu?
- Tarama sonunda rapor olusuyor mu?

## 6) Not
`icd_runtime_template.json` genis kapsamli saha dokumanidir.
Uygulamanin bugunku cekirdek baglanti anahtari `config/activation.json` dosyasidir.
ICD geldikce bu iki dosya birlikte guncellenmelidir.
