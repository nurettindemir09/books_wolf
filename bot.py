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
import os

# Global logger callback
STOP_BOT = False

def log(msg, callback=None):
    if callback:
        try:
            callback(str(msg))
        except: pass
    print(msg)

def init_driver(log_callback=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        log(f"Failed to initialize driver: {e}", log_callback)
        return None

def fill_field(driver, field_key, value, by_method=By.NAME, hit_enter=False, log_callback=None):
    """Helper to fill a field safely."""
    if not value: 
        return
    
    selector = config.FIELDS.get(field_key)
    if not selector: return

    log(f"   -> Filling {field_key} with '{value}'...", log_callback)

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
                except: log(f"      Could not select '{value}' for {field_key}", log_callback)
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
                                log(f"      [✓] Clicked exact match for '{value}'", log_callback)
                                break
                    except Exception as match_err:
                        log(f"      [!] Match click failed: {match_err}", log_callback)
                    
                    if not found_click:
                        log(f"      [!] Exact match not found visible. Trying ENTER...", log_callback)
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
            log(f"      [X] Failed to fill {field_key}: {e}", log_callback)

def fill_form(driver, student, log_callback=None):
    try:
        # 1. Names (Critical)
        fill_field(driver, 'firstname', student['first_name'], By.NAME, log_callback=log_callback)
        fill_field(driver, 'lastname', student['last_name'], By.NAME, log_callback=log_callback)
        fill_field(driver, 'tckn', student['tckn'], By.NAME, log_callback=log_callback)
        
        # Birthdate
        fill_field(driver, 'birthdate', student['birth_date'], By.NAME, log_callback=log_callback)

        # Phone
        fill_field(driver, 'phone', student.get('phone'), By.NAME, log_callback=log_callback)

        # Gender (Guess if missing)
        gender = student.get('gender', '')
        if not gender:
            gender = gender_guesser.guess_gender(student['first_name'])
        
        fill_field(driver, 'gender', gender, By.NAME, hit_enter=True, log_callback=log_callback)
        
        # Residence (Hit Enter for autocomplete)
        fill_field(driver, 'res_city', student.get('res_city'), By.NAME, hit_enter=True, log_callback=log_callback)
        fill_field(driver, 'res_district', student.get('res_district'), By.NAME, hit_enter=True, log_callback=log_callback)
        
        # School
        fill_field(driver, 'school_city', student.get('school_city'), By.NAME, hit_enter=True, log_callback=log_callback)
        fill_field(driver, 'school_county', student.get('school_county'), By.NAME, hit_enter=True, log_callback=log_callback)
        fill_field(driver, 'school_name', student.get('school_name'), By.NAME, hit_enter=True, log_callback=log_callback)
        
        # Class
        fill_field(driver, 'class_name', student.get('class_info'), By.NAME, hit_enter=True, log_callback=log_callback)
        
        # Parent
        fill_field(driver, 'parent_name', student.get('parent_name'), By.NAME, log_callback=log_callback)
        fill_field(driver, 'parent_phone', student.get('parent_phone'), By.NAME, log_callback=log_callback)
        
        # Reference
        fill_field(driver, 'ref_teacher_name', student.get('ref_teacher_name'), By.NAME, log_callback=log_callback)
        fill_field(driver, 'ref_teacher_phone', student.get('ref_teacher_phone'), By.NAME, log_callback=log_callback)
        
        # Disability
        fill_field(driver, 'disability', student.get('disability'), By.NAME, log_callback=log_callback)

        # KVKK
        try:
            checkbox = driver.find_element(By.ID, config.FIELDS['kvkk'])
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", checkbox)
            time.sleep(0.5)
            if not checkbox.is_selected():
                checkbox.click()
        except:
            try:
                kvkk_text = driver.find_element(By.XPATH, "//*[contains(text(), 'KVKK Aydınlatma Metni')]")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", kvkk_text)
                time.sleep(0.5)
                kvkk_text.click() 
            except Exception as e:
                log(f"      [!] Could not check KVKK: {e}", log_callback)

        # CAPTCHA Focus
        try:
            captcha_input = driver.find_element(By.XPATH, "((//span[contains(text(), 'Enter the characters')] | //label[contains(text(), 'Enter the characters')])/following::input[@type='text'])[1]")
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", captcha_input)
            time.sleep(0.2)
            captcha_input.click()
            log("      [i] CAPTCHA input focused. Type the characters and press Enter.", log_callback)
            
        except Exception as e:
            try:
                 captcha_input = driver.find_element(By.XPATH, "//input[contains(@id, 'captcha') or contains(@name, 'captcha')]")
                 driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", captcha_input)
                 captcha_input.click()
                 log("      [i] CAPTCHA input focused (fallback).", log_callback)
            except:
                 log(f"      [!] Could not auto-focus CAPTCHA: {e}", log_callback) 
                 
    except Exception as e:
        log(f"Error in main form fill: {e}", log_callback)

def run_bot(data_file_path, log_callback=None):
    global STOP_BOT
    STOP_BOT = False
    
    log("\n" + "="*40, log_callback)
    log("      BOT VERSION 2.0 (GUI SUPPORTED)", log_callback)
    log("="*40 + "\n", log_callback)
    
    log(f"Reading {data_file_path}...", log_callback)
    students = excel_handler.load_data(data_file_path)
    
    if not students:
        log(f"ERROR: Could not read '{data_file_path}'.", log_callback)
        return

    log(f"Loaded {len(students)} students from file.", log_callback)
    
    # Load completed TCKNs
    completed_tckns = set()
    if os.path.exists('completed.txt'):
         with open('completed.txt', 'r') as f:
             completed_tckns = {line.strip() for line in f if line.strip()}
    log(f"Loaded {len(completed_tckns)} previously completed students.", log_callback)

    driver = init_driver(log_callback)
    if not driver: return

    try:
        total_students = len(students)
        
        for i, student in enumerate(students, 1):
            if STOP_BOT:
                log("Bot stopped by user.", log_callback)
                break
                
            tckn = student.get('tckn', '').strip()
            full_name = f"{student['first_name']} {student['last_name']}"
            
            if tckn in completed_tckns:
                log(f"Skipping {i}/{total_students}: {full_name} (Already completed)", log_callback)
                continue
                
            log(f"\nProcessing {i}/{total_students}: {full_name}", log_callback)
            driver.get(config.URL)
            time.sleep(2)
            
            fill_form(driver, student, log_callback)
            
            log("\n>> Form filled. CAPTCHA focused.", log_callback)
            log(">> ACTION REQUIRED: Type CAPTCHA and Click 'GÖNDER' (Submit).", log_callback)
            log(">> Bot is watching for 'Başvurunuz başarıyla alınmıştır' message...", log_callback)

            # Wait for success message or user skip
            success_detected = False
            
            while True:
                if STOP_BOT: break
                    
                try:
                    success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Başvurunuz başarıyla alınmıştır')]")
                    for elem in success_elements:
                        if elem.is_displayed():
                            log(f"   [+] Success detected for {student['first_name']}!", log_callback)
                            success_detected = True
                            
                            # Save to completed
                            if tckn:
                                with open('completed.txt', 'a') as f:
                                    f.write(tckn + '\n')
                                completed_tckns.add(tckn)
                            break
                    
                    if success_detected: break

                except: pass
                
                if not driver.window_handles: 
                    return

                time.sleep(1)

            if success_detected:
                log("   [i] Success confirmed. Waiting 1.5 seconds before next student...", log_callback)
                time.sleep(1.5)
            
    except KeyboardInterrupt:
        log("\nStopped.", log_callback)
    except Exception as e:
        log(f"Critical Error: {e}", log_callback)
    finally:
        if driver: driver.quit()
        log("Bot Finished/Stopped.", log_callback)

if __name__ == "__main__":
    # Default behavior for CLI
    run_bot("veriler.csv")
