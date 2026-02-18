# Books Wolf - Otomatik Başvuru Botu

Bu proje, ******************** başvurularını otomatize etmek için geliştirilmiş bir Python botudur. Excel veya CSV dosyasındaki öğrenci verilerini okuyarak web formunu otomatik olarak doldurur.

## Özellikler

*   **CSV ve Excel Desteği:** `veriler.csv` (noktalı virgül ayracı ile) veya `veriler.xlsx` dosyalarından veri okuyabilir.
*   **Akıllı Cinsiyet Tahmini:** İsimden cinsiyet tahmini yaparak (Erkek/Kadın) formu doldurur.
*   **Otomatik Seçim:** İl, ilçe, okul ve sınıf gibi açılır menüleri akıllıca arayıp seçer (Tam eşleşme kontrolü).
*   **CAPTCHA Yardımı:** Form doldurulduktan sonra otomatik olarak CAPTCHA kutusuna odaklanır, böylece sadece karakterleri yazıp `Enter` tuşuna basmanız yeterlidir.
*   **Seri Doldurma:** Başvuru başarıyla tamamlandığında ("Başvurunuz başarıyla alınmıştır" mesajını görünce) otomatik olarak bir sonraki öğrenciye geçer.

## Kurulum 

Eğer bu botu başka bir bilgisayarda çalıştırmak isterseniz sırasıyla şunları yapmalısınız:

1.  **Python Yükleyin:**
    *   [python.org](https://www.python.org/downloads/) adresinden Python'un son sürümünü indirin ve kurun.
    *   **ÖNEMLİ:** Kurulum sırasında **"Add Python to PATH"** kutucuğunu MUTLAKA işaretleyin.

2.  **Projeyi İndirin:**
    *   Bu sayfadan **Code -> Download ZIP** diyerek dosyaları indirin ve masaüstüne klasör olarak çıkarın.
    *   Veya terminalden: `git clone https://github.com/nurettindemir09/books_wolf.git`

3.  **Gerekli Kütüphaneleri Yükleyin:**
    *   Proje klasörünün içine girin.
    *   Klasörde boş bir yere `Shift + Sağ Tık` yapıp **"PowerShell penceresini buradan aç"** veya **"Terminalde aç"** deyin.
    *   Şu komutu yapıştırıp `Enter`'a basın:
        ```bash
        pip install pandas selenium openpyxl webdriver-manager image
        ```

4.  **Hazırsınız!**
    *   Artık `baslat.bat` dosyasına çift tıklayarak botu açabilirsiniz.

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
