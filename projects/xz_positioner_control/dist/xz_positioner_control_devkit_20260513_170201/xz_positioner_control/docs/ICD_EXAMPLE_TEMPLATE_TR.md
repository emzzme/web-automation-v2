# ICD Ornek Format (XZ Pozisyoner RF Olcum)

## 1) Dokuman Bilgisi
- Dokuman No: ICD-XZRF-001
- Revizyon: A
- Tarih: 2026-05-04
- Taraflar: YUKLENICI / MUSTERI

## 2) Sistem Sinirlari
- Controller Unit
- Control PC (GUI)
- VNA
- TTL I/O
- X/Z Axis Drivers

## 3) Fiziksel Arayuzler
### 3.1 Controller <-> PC
- Transport: Ethernet / USB
- Ethernet: IPv4, Port, Protocol (TCP/UDP)
- USB: COM Port, Baudrate, Parity, Stop Bit

### 3.2 PC <-> VNA
- Transport: LAN or USBTMC
- Protocol: SCPI
- VISA Resource Name: (ornek) TCPIP0::10.0.21.151::inst0::INSTR

### 3.3 Controller <-> TTL I/O
- Trigger OUT pin map
- E-Stop IN pin map
- X/Z limit & home pin map

## 4) Mesaj / Komut Sozlesmesi
### 4.1 Hareket Komutlari
- MOVE X <target_mm>
- MOVE Z <target_mm>
- STOP
- HOME
- PARK

### 4.2 Durum Komutlari
- READ X
- READ Z
- READ STATUS
- READ ALARMS

### 4.3 VNA SCPI Komutlari
- *IDN?
- SENS:FREQ:STAR <GHz>
- SENS:FREQ:STOP <GHz>
- SENS:SWE:POIN <N>
- CALC:PAR:DEF 'Trc1','S21'
- INIT:IMM; *OPC?

## 5) Zamanlama ve Senkronizasyon
- Controller command timeout
- Retry policy
- Step noktasinda TTL pulse genisligi ve seviyesi
- VNA trigger latency budget

## 6) Emniyet ve Alarm Kodlari
- ESTOP_LATCHED
- LIMIT_ACTIVE
- WATCHDOG_TIMEOUT
- SCPI_TIMEOUT

## 7) Dogrulama Prosedurleri
- Baglanti testleri
- Komut echo/ack testleri
- Hareket, limit, estop fonksiyon testi
- SCPI trace alma testi
- TTL pulse ve input okuma testi

## 8) Konfigurasyon Ornekleri
### activation.json
```json
{
  "controller_transport": "USB",
  "controller_target": "COM5",
  "vna_transport": "LAN",
  "vna_target": "10.0.21.151",
  "trigger_mode": "TTL_STEP"
}
```

### command_map.json
```json
{
  "move_abs_template": "MOVE {axis} {target_mm:.3f}",
  "stop_cmd": "STOP",
  "read_axis_template": "READ {axis}"
}
```
