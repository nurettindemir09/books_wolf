import pandas as pd

data = {
    'Sinif_Sube': ['8. Sınıf / A Şubesi', '8. Sınıf / A Şubesi'],
    'TCKN': ['43120029810', '25543618420'],
    'Ogrenci_No': [19, 43],
    'Ad_Soyad': ['ŞERVAN ZEYBEK', 'MUHAMMET EREN DEMİROK'],
    'Dogum_Tarihi': ['27/08/2012', '08/10/2012']
}

df = pd.DataFrame(data)
df.to_excel('data.xlsx', index=False)
print("data.xlsx created.")
