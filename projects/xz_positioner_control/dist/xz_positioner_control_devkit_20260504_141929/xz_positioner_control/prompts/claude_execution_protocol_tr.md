# Claude Execution Protocol (TR)

## Amac
Claude code oturumlarinda token kesilmesi olsa bile isler yarim kalmasin, bir sonraki oturumda otomatik devam edilsin.

## Kurallar
1. Her gorev sonunda durum `state/pipeline_state.json` dosyasina checkpoint yaz.
2. Her adim idempotent olacak sekilde tasarla (tekrar calissa zarar vermesin).
3. Buyuk isi kucuk adimlara bol (en fazla 6 adimlik sprint bloklari).
4. Her adim bitince dogrulama komutunu calistir ve sonucu state'e yaz.
5. Kesmeye dayanmak icin tum ciktilari dosya odakli uret.

## Zorunlu Cikti Sablonu
- Degisen dosyalar
- Yapilan islemler
- Kalan isler
- Sonraki oturum ilk komutu

## Otomatik Devam Komutu
`python scripts/resumable_pipeline.py --root . --icd <opsiyonel_dosya>`

## Build ve Paketleme
1. `powershell -ExecutionPolicy Bypass -File scripts/bootstrap_and_build.ps1`
2. Opsiyonel setup.exe: `powershell -ExecutionPolicy Bypass -File scripts/make_setup.ps1`
