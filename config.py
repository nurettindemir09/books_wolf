# Form Config
URL = "https://basvuru.tugva.org/kitap-kurdu/"

# Field Selectors (By ID or Name)
FIELDS = {
    'firstname': 'firstname', # Name attribute
    'lastname': 'lastname',   # Name attribute
    'tckn': 'tgv_identificationnumber', # Name attribute
    'birthdate': 'tgv_birthdate', # Name attribute
    'phone': 'mobilephone', # Name attribute
    'gender': 'tgv_gendercode', # Select Name
    'nationality': 'tgv_nationality', # Select Name
    'res_city': 'tgv_residencecity', # Name attribute (Input?)
    'res_district': 'tgv_residencedistrict', # Name attribute
    'school_city': 'tgv_schoolcity', # Name attribute
    'school_county': 'tgv_schoolcounty', # Name attribute
    'school_name': 'tgv_schoolid', # Name attribute or ID? Careful with dynamic search
    'school_exists': 'tgv_existschool', # Radio
    'unknown_school': 'tgv_unknownschool', # Input
    'class_name': 'tgv_classid', # Input
    'parent_name': 'tgv_parentnamesurname', # Input
    'parent_phone': 'tgv_parenttelephone', # Input
    'ref_teacher_name': 'tgv_refetanceteachername', # Input
    'ref_teacher_phone': 'tgv_referancemobilenumber', # Input
    'disability': 'tgv_disabledstatus', # Select
    'kvkk': 'kvkkCheckbox', # ID
}

# Optional: Default Values to auto-fill if missing in Excel
# Leave empty string "" to skip auto-filling
DEFAULTS = {
    'gender': '', # 1: Male, 2: Female (Need to check value codes)
    'nationality': '1', # Assuming 1 is TC? Check value codes
    'res_city': '', 
    'res_district': '',
    'school_city': '',
    'school_county': '',
    'school_name': '',
    'parent_name': '', 
    'parent_phone': '' 
}
