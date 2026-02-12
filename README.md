# Books Wolf - Otomatik Başvuru Botu

Bu proje, **Tügva Kitap Kurdu** başvurularını otomatize etmek için geliştirilmiş bir Python botudur. Excel veya CSV dosyasındaki öğrenci verilerini okuyarak web formunu otomatik olarak doldurur.

## Özellikler

*   **CSV ve Excel Desteği:** `veriler.csv` (noktalı virgül ayracı ile) veya `veriler.xlsx` dosyalarından veri okuyabilir.
*   **Akıllı Cinsiyet Tahmini:** İsimden cinsiyet tahmini yaparak (Erkek/Kadın) formu doldurur.
*   **Otomatik Seçim:** İl, ilçe, okul ve sınıf gibi açılır menüleri akıllıca arayıp seçer (Tam eşleşme kontrolü).
*   **CAPTCHA Yardımı:** Form doldurulduktan sonra otomatik olarak CAPTCHA kutusuna odaklanır, böylece sadece karakterleri yazıp `Enter` tuşuna basmanız yeterlidir.
*   **Seri Doldurma:** Başvuru başarıyla tamamlandığında ("Başvurunuz başarıyla alınmıştır" mesajını görünce) otomatik olarak bir sonraki öğrenciye geçer.

## Kurulum

1.  Python'u yükleyin.
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install pandas selenium openpyxl
    ```
3.  Chrome tarayıcınızın güncel olduğundan emin olun.

## Kullanım (Kolay Arayüz ile)

1.  **`baslat.bat`** dosyasına çift tıklayın.
2.  Açılan pencerede **"Dosya Seç"** butonuna basarak öğrenci listenizi (CSV veya Excel) seçin.
3.  **"BOTU BAŞLAT"** butonuna basın.
4.  Bot çalışmaya başlayacak ve işlem kayıtlarını pencerede gösterecektir.

## Kullanım (Terminal ile)

1.  `veriler.csv` dosyasını hazırlayın.
2.  Botu çalıştırın:
    ```bash
    python bot.py
    ```


## Notlar

*   **KVKK:** KVKK kutucuğu otomatik onaylanır.
*   **Okul Seçimi:** Okul adı girilir ancak "Listede Okulum Var/Yok" seçeneğine dokunulmaz (Varsayılan bırakılır).
