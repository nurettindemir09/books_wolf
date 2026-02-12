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

## Kullanım

1.  `veriler.csv` dosyasını hazırlayın (Örnek format proje içinde mevcuttur).
2.  Botu çalıştırın:
    ```bash
    python bot.py
    ```
3.  Açılan tarayıcıda bot formu dolduracaktır. CAPTCHA alanına gelince karakterleri girip `Enter` veya `Gönder` butonuna basın.
4.  Bot başarı mesajını algılayıp diğer öğrenciye geçecektir.

## Notlar

*   **KVKK:** KVKK kutucuğu otomatik onaylanır.
*   **Okul Seçimi:** Okul adı girilir ancak "Listede Okulum Var/Yok" seçeneğine dokunulmaz (Varsayılan bırakılır).
