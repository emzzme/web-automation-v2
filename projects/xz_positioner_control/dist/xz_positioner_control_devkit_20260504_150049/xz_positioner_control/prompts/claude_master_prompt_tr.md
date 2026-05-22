# Claude Master Prompt (TR)

Asagidaki gorevi bir endustriyel yazilim ekibi kalitesinde, adim adim ve calisir kod ureterek tamamla.

## Misyon
Windows tabanli komuta-kontrol bilgisayarinda calisacak, Python + PySide6 ile yazilmis bir "XZ Lineer Pozisyoner RF Olcum Ana Kontrol Arayuzu" gelistir.

## Tasarim Yonu
- Referans ekran: kullanicinin paylastigi gorsele yakin panel yapisi
- Sol menu + ust durum cubugu + orta kontrol kartlari + sag/alt grafik panelleri
- Endustriyel, net, okunabilir UI (abartili animasyon yok)
- Operatorun kritik bilgiyi 1 bakista gorecegi duzen

## Teknik Kisitlar
1. Dil: Python 3.11+
2. UI: PySide6
3. Grafikler: pyqtgraph
4. Mimari: katmanli, interface tabanli, test edilebilir
5. Gercek donanim yoksa mock driver ile tam calisan demo

## Moduller
1. Manuel Kontrol
- X/Z anlik konum
- Jog -, Jog +, Stop, Home, Park
- Hiz/ivme ayari

2. Tarama Reçetesi
- X/Z baslangic-bitis-adim
- Snaking secenegi
- Tahmini sure ve nokta sayisi

3. VNA Kontrol
- IP/SCPI baglantisi
- Start/Stop freq, IFBW, power
- Canli S21 trace

4. Otomatik Tarama
- Baslat/Duraklat/Devam/Durdur/Abort
- Ilerleme cubugu
- Islem adimlari (moving/setting/triggering/measuring/saving)

5. Veri ve Log
- Alarm/Log tablosu
- Olcum kayit klasoru
- CSV + metadata export

## Emniyet Kurallari
- X/Z soft limit disina cikma engeli
- Hata halinde otomatik stop
- Timeout ve retry mekanizmasi
- Tum kritik olaylar loglansin

## Kod Kalite Beklentisi
- Her modulu ayri dosyalarda yaz
- Tip ipuclari kullan
- Acik ve kisa fonksiyonlar yaz
- UI islemleri ile donanim islemlerini ayir
- Mock ve real driver switch mekanizmasi koy

## Teslimat Sirasi
1. Klasor yapisini olustur
2. Calisir ana pencereyi cikar
3. Mock servislerle canli veri goster
4. Donanim interface katmanini tanimla
5. Unit testlerden kritik olanlari ekle
6. Kurulum ve calistirma adimlarini yaz

## Cikti Formati
- Once degistirdigin dosyalari listele
- Sonra kodu dosya dosya ver
- En sonda calistirma komutlarini tek blokta ver
- Eger bir varsayim yaptiysan "Varsayimlar" basligi altinda yaz

## Oncelik
Calismayan buyuk kod yerine, her adimda calisan ve test edilebilir artimlar uret.
