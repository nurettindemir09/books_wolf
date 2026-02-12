import time
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("Selenium not found. Please run 'pip install selenium webdriver-manager'")
    exit()

import config
import excel_handler
import gender_guesser

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Failed to initialize driver: {e}")
        return None

def fill_field(driver, field_key, value, by_method=By.NAME, hit_enter=False):
    """Helper to fill a field safely."""
    if not value: 
        # print(f"Skipping {field_key} (Empty value)")
        return
    
    selector = config.FIELDS.get(field_key)
    if not selector: return

    print(f"   -> Filling {field_key} with '{value}'...")

    try:
        wait = WebDriverWait(driver, 5)
        # Try finding element
        element = wait.until(EC.element_to_be_clickable((by_method, selector)))
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5) # Wait for scroll
        
        element.click()
        
        tag_name = element.tag_name.lower()
        
        if tag_name == 'select':
            from selenium.webdriver.support.ui import Select
            select = Select(element)
            try: 
                select.select_by_visible_text(value)
            except:
                try: select.select_by_value(value)
                except: print(f"      Could not select '{value}' for {field_key}")
        else:
            # Check if it has a value already?
            current_val = element.get_attribute('value')
            if current_val != value:
                # For inputs that need selection from a dropdown (hit_enter=True)
                if hit_enter:
                    element.clear()
                    time.sleep(0.2)
                    element.send_keys(value)
                    time.sleep(1.5) # Wait for results to load
                    
                    found_click = False
                    try:
                        # Try to find an element with the exact text (ignoring the input itself)
                        # We look for common dropdown item tags: li, div, span, a
                        xpath_expr = f"//*[(self::li or self::div or self::span or self::a) and normalize-space(text())='{value}']"
                        possible_items = driver.find_elements(By.XPATH, xpath_expr)
                        
                        for item in possible_items:
                            if item.is_displayed():
                                # Scroll to it
                                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item)
                                time.sleep(0.2)
                                item.click()
                                found_click = True
                                print(f"      [✓] Clicked exact match for '{value}'")
                                break
                    except Exception as match_err:
                        print(f"      [!] Match click failed: {match_err}")
                    
                    if not found_click:
                        # Fallback: Just hitting Enter (sometimes Down+Enter is bad if 1st result is wrong)
                        # User said: "First result is being selected, we don't want this". 
                        # This implies we shouldn't force select index 0. 
                        # But if we typed the exact name, maybe just ENTER is enough?
                        # Let's try sending Enter without Down first.
                        print(f"      [!] Exact match not found visible. Trying ENTER...")
                        element.send_keys(Keys.ENTER)
                    
                    time.sleep(0.5)
                else:
                    element.clear()
                    element.send_keys(value)
            
    except Exception as e:
        # Retry with Name if ID failed, or vice versa
        try:
            alt_method = By.NAME if by_method == By.ID else By.ID
            element = driver.find_element(alt_method, selector)
            element.send_keys(value)
        except:
            print(f"      [X] Failed to fill {field_key}: {e}")

def fill_form(driver, student):
    try:
        # 1. Names (Critical)
        fill_field(driver, 'firstname', student['first_name'], By.NAME)
        fill_field(driver, 'lastname', student['last_name'], By.NAME)
        fill_field(driver, 'tckn', student['tckn'], By.NAME)
        
        # Birthdate
        fill_field(driver, 'birthdate', student['birth_date'], By.NAME)

        # Phone
        fill_field(driver, 'phone', student.get('phone'), By.NAME)

        # Gender (Guess if missing)
        gender = student.get('gender', '')
        if not gender:
            gender = gender_guesser.guess_gender(student['first_name'])
        
        fill_field(driver, 'gender', gender, By.NAME, hit_enter=True)
        
        # Residence (Hit Enter for autocomplete)
        fill_field(driver, 'res_city', student.get('res_city'), By.NAME, hit_enter=True)
        fill_field(driver, 'res_district', student.get('res_district'), By.NAME, hit_enter=True)
        
        # School
        fill_field(driver, 'school_city', student.get('school_city'), By.NAME, hit_enter=True)
        fill_field(driver, 'school_county', student.get('school_county'), By.NAME, hit_enter=True)
        fill_field(driver, 'school_name', student.get('school_name'), By.NAME, hit_enter=True)
        
        # Check Radio for "School Exists" -> usually Value 1
        # try:
        #     # Try to click the "Okulum var" or similar radio if needed.
        #     # Assuming first radio is "Exists"
        #     radios = driver.find_elements(By.NAME, config.FIELDS['school_exists'])
        #     if radios: radios[0].click()
        # except: pass

        # Class
        fill_field(driver, 'class_name', student.get('class_info'), By.NAME, hit_enter=True)
        
        # Parent
        fill_field(driver, 'parent_name', student.get('parent_name'), By.NAME)
        fill_field(driver, 'parent_phone', student.get('parent_phone'), By.NAME)
        
        # Reference
        fill_field(driver, 'ref_teacher_name', student.get('ref_teacher_name'), By.NAME)
        fill_field(driver, 'ref_teacher_phone', student.get('ref_teacher_phone'), By.NAME)
        
        # Disability
        fill_field(driver, 'disability', student.get('disability'), By.NAME)

        # KVKK
        try:
            # Try by ID first
            checkbox = driver.find_element(By.ID, config.FIELDS['kvkk'])
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", checkbox)
            time.sleep(0.5)
            if not checkbox.is_selected():
                checkbox.click()
        except:
            try:
                # Try by Text
                kvkk_text = driver.find_element(By.XPATH, "//*[contains(text(), 'KVKK Aydınlatma Metni')]")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", kvkk_text)
                time.sleep(0.5)
                kvkk_text.click() # Clicking text often checks the box
            except Exception as e:
                print(f"      [!] Could not check KVKK: {e}")

        # CAPTCHA Focus
        try:
            # Find input near "Enter the characters you see"
            # Strategy: Find the label/text, then find the following input
            captcha_input = driver.find_element(By.XPATH, "((//span[contains(text(), 'Enter the characters')] | //label[contains(text(), 'Enter the characters')])/following::input[@type='text'])[1]")
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", captcha_input)
            time.sleep(0.2)
            captcha_input.click()
            print("      [i] CAPTCHA input focused. Type the characters and press Enter.")
            
        except Exception as e:
            # Fallback for alternative layout
            try:
                 # Look for input with 'captcha' in ID or Name
                 captcha_input = driver.find_element(By.XPATH, "//input[contains(@id, 'captcha') or contains(@name, 'captcha')]")
                 driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", captcha_input)
                 captcha_input.click()
                 print("      [i] CAPTCHA input focused (fallback).")
            except:
                 print(f"      [!] Could not auto-focus CAPTCHA: {e}") 
                 
    except Exception as e:
        print(f"Error in main form fill: {e}")

def main():
    print("\n" + "="*40)
    print("      BOT VERSION 2.0 (UPDATED)")
    print("="*40 + "\n")
    
    print("Reading veriler.csv...")
    students = excel_handler.load_data('veriler.csv')
    
    if not students:
        print("ERROR: Could not read 'veriler.csv'. Please make sure the file exists and is closed.")
        # Fallback check
        import os
        if os.path.exists('veriler.xlsx'):
             print("Found 'veriler.xlsx' but defaulting to 'veriler.csv'.")
        return

    print(f"Loaded {len(students)} students from veriler.csv.")
    
    # Load completed TCKNs
    completed_tckns = set()
    if os.path.exists('completed.txt'):
         with open('completed.txt', 'r') as f:
             completed_tckns = {line.strip() for line in f if line.strip()}
    print(f"Loaded {len(completed_tckns)} previously completed students.")

    try:
        total_students = len(students)
        
        # Remove hardcoded skip, rely on completed_tckns
        # process_list = students[1:] 
        
        for i, student in enumerate(students, 1):
            tckn = student.get('tckn', '').strip()
            full_name = f"{student['first_name']} {student['last_name']}"
            
            if tckn in completed_tckns:
                print(f"Skipping {i}/{total_students}: {full_name} (Already completed)")
                continue
                
            print(f"\nProcessing {i}/{total_students}: {full_name}")
            driver.get(config.URL)
            time.sleep(2)
            
            fill_form(driver, student)
            
            print("\n>> Form filled. CAPTCHA focused.")
            print(">> ACTION REQUIRED: Type CAPTCHA and Click 'GÖNDER' (Submit).")
            print(">> Bot is watching for 'Başvurunuz başarıyla alınmıştır' message...")

            # Wait for success message or user skip
            success_detected = False
            
            while True:
                try:
                    # Check for Success Message - MUST BE VISIBLE
                    # Use XPath to find the element containing the specific text AND is visible
                    success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Başvurunuz başarıyla alınmıştır')]")
                    
                    for elem in success_elements:
                        if elem.is_displayed():
                            print(f"   [+] Success detected for {student['first_name']}!")
                            success_detected = True
                            
                            # Save to completed
                            if tckn:
                                with open('completed.txt', 'a') as f:
                                    f.write(tckn + '\n')
                                completed_tckns.add(tckn)
                            break
                    
                    if success_detected: break

                except: pass
                
                # Allow user to interrupt or check manual close
                if not driver.window_handles: # Browser closed
                    return

                time.sleep(1)

            if success_detected:
                print("   [i] Success confirmed. Waiting 1.5 seconds before next student...")
                time.sleep(1.5)
            
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    main()
