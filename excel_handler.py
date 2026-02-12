import pandas as pd
from datetime import datetime
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    try:
        # Check extension
        is_csv = file_path.lower().endswith('.csv')

        if is_csv:
            # Read CSV with ; delimiter (common in Turkish CSVs) and keep as string
            df = pd.read_csv(file_path, sep=';', dtype=str)
        else:
            df = pd.read_excel(file_path, dtype=str)
    except Exception as e:
        print(f"File read error: {e}")
        return []

    students = []
    
    # Check if this is the OLD data format (data.xlsx)
    is_old_format = 'Ad_Soyad' in df.columns
    
    # Handle NaN values by filling with empty string
    df = df.fillna('')

    for _, row in df.iterrows():
        student = {}
        
        if is_old_format:
            # Legacy support (Old data.xlsx)
            fullname = str(row.get('Ad_Soyad', '')).strip()
            if ' ' in fullname:
                student['first_name'] = fullname.rsplit(' ', 1)[0]
                student['last_name'] = fullname.rsplit(' ', 1)[1]
            else:
                student['first_name'] = fullname
                student['last_name'] = ''
            student['tckn'] = str(row.get('TCKN', ''))
            student['birth_date'] = str(row.get('Dogum_Tarihi', '')).split(' ')[0]
        else:
            # NEW FORMAT (veriler.xlsx / veriler.csv)
            # Use .strip() to handle potential column name whitespace
            
            # Helper to safely get value from row with stripped keys
            def get_val(key):
                # Direct lookup
                if key in row: return str(row[key]).strip()
                # Case-insensitive / Strip lookup
                for col in df.columns:
                    if col.strip() == key:
                        return str(row[col]).strip()
                return ''

            student['first_name'] = get_val('Ad')
            student['last_name'] = get_val('Soyad')
            student['tckn'] = get_val('TC Kimlik No / Pasaport No').replace('.0', '')
            
            # Date Parsing
            dob = get_val('Doğum Tarihi')
            try:
                if ' ' in dob: dob = dob.split(' ')[0]
                # Convert standard formats to dd.mm.yyyy
                if '/' in dob: 
                    # 25/09/2015 -> 25.09.2015
                    dob = dob.replace('/', '.')
                elif '-' in dob: 
                    # yyyy-mm-dd -> dd.mm.yyyy
                    d = datetime.strptime(dob, '%Y-%m-%d')
                    dob = d.strftime('%d.%m.%Y')
            except: pass
            student['birth_date'] = dob
            
            student['phone'] = get_val('Telefon').replace('.0', '')
            student['res_city'] = get_val('İkamet Adres İli') # Note: 'İli' not 'İl' in CSV
            student['res_district'] = get_val('İkamet Adres İlçe')
            student['school_city'] = get_val('Okul İli') # Note: 'İli' not 'İl'
            student['school_county'] = get_val('Okul İlçe')
            student['school_name'] = get_val('Okul')
            student['class_info'] = get_val('Sınıf')
            student['parent_name'] = get_val('Veli Ad Soyad')
            student['parent_phone'] = get_val('Veli Telefon').replace('.0', '')
            student['disability'] = get_val('Engel Durumu')
            student['ref_teacher_name'] = get_val('Danışman Öğretmen Ad Soyad')
            student['ref_teacher_phone'] = get_val('Danışman Öğretmen Telefon').replace('.0', '')
            
        students.append(student)
        
    return students

