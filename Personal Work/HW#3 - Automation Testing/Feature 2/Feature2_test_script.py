from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from openpyxl.workbook import Workbook
import time
import csv
import pandas as pd
import os

# 1. Kết nối và truy cập trang web
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get("http://localhost:8080/orangehrm-4.5/symfony/web/index.php/admin/viewOrganizationGeneralInformation")

test_results = []


# 2. Đăng nhập vào trang Web
time.sleep(2)
username_field = driver.find_element(By.ID, 'txtUsername')
username_field.send_keys("Admin")

password_field = driver.find_element(By.ID, "txtPassword")
password_field.send_keys("suViet99.000")

password_field.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)
edit_button = wait.until(EC.visibility_of_element_located((By.ID, "btnSaveGenInfo")))

# 3. Click vào button "Edit"
edit_button.click()

time.sleep(2)
# 4. Đọc dữ liệu từ file CSV
with open('Feature2_test_data.csv', newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        tc = row['No']
        on = row['Organization Name']
        ti = row['Tax ID']
        rn = row['Registration Number']
        p = row['Phone']
        e = row['Email']
        f = row['Fax']
        at1 = row['Address Street 1']
        c = row['City']
        zp = row['Zip/Postal Code']
        no = row['Note']
        at2 = row['Address Street 2']
        sp = row['State/Province']
        er = row['Expected Result']

        print([tc, on, ti, rn, p, e, f, at1, c, zp, no, at2, sp, er])
                
        organization = driver.find_element(By.ID, "organization_name")
        organization.clear()
        organization.send_keys(on)

        organization_taxId = driver.find_element(By.ID, "organization_taxId")
        organization_taxId.clear()
        organization_taxId.send_keys(ti)

        organization_registraionNumber = driver.find_element(By.ID, "organization_registraionNumber")
        organization_registraionNumber.clear()
        organization_registraionNumber.send_keys(rn)

        organization_phone = driver.find_element(By.ID, "organization_phone")
        organization_phone.clear()
        organization_phone.send_keys(p)

        organization_email = driver.find_element(By.ID, "organization_email")
        organization_email.clear()
        organization_email.send_keys(e)

        organization_fax = driver.find_element(By.ID, "organization_fax")
        organization_fax.clear()
        organization_fax.send_keys(f)

        organization_street1 = driver.find_element(By.ID, "organization_street1")
        organization_street1.clear()
        organization_street1.send_keys(at1)

        organization_city = driver.find_element(By.ID, "organization_city")
        organization_city.clear()
        organization_city.send_keys(c)

        organization_zipCode = driver.find_element(By.ID, "organization_zipCode")
        organization_zipCode.clear()
        organization_zipCode.send_keys(zp)

        organization_note = driver.find_element(By.ID, "organization_note")
        organization_note.clear()
        organization_note.send_keys(no)

        organization_street2 = driver.find_element(By.ID, "organization_street2")
        organization_street2.clear()
        organization_street2.send_keys(at2)

        organization_province = driver.find_element(By.ID, "organization_province")
        organization_province.clear()
        organization_province.send_keys(sp)


        # 5. Click vào button "Save" để lưu thông tin đã chỉnh sửa
        wait = WebDriverWait(driver, 10)
        save_button = wait.until(EC.visibility_of_element_located((By.ID, "btnSaveGenInfo")))
        save_button.click()
                
        time.sleep(10)
        driver.implicitly_wait(10)  

        # 6. Kiểm tra trạng thái sau khi edit thành công
        wait = WebDriverWait(driver, 10)
        soe_button = wait.until(EC.visibility_of_element_located((By.ID, "btnSaveGenInfo")))

        target_value = "Edit"
        current = soe_button.get_attribute('value')
        print(current)
        if current == target_value:
            print("Thao tác edit thành công.\n")
            test_results.append({'No': tc, 'Organization Name': on, 'Tax ID': ti, 'Registration Number': rn, 'Phone': p, 'Email': e, 'Fax': f, 'Address Street 1': at1, 'City': c, 'Zip/Postal Code': zp, 'Note': no, 'Address Street 2': at2, 'State/Province': sp, 'Expected Result': er, 'Actual Result': 'Passed'})
        else:
            print("Thao tác edit thất bại.\n")
            test_results.append({'No': tc, 'Organization Name': on, 'Tax ID': ti, 'Registration Number': rn, 'Phone': p, 'Email': e, 'Fax': f, 'Address Street 1': at1, 'City': c, 'Zip/Postal Code': zp, 'Note': no, 'Address Street 2': at2, 'State/Province': sp, 'Expected Result': er, 'Actual Result': 'Failed'})        
        
        driver.get("http://localhost:8080/orangehrm-4.5/symfony/web/index.php/admin/viewOrganizationGeneralInformation")
        wait = WebDriverWait(driver, 10)
        edit_button = wait.until(EC.visibility_of_element_located((By.ID, "btnSaveGenInfo")))

        # Click vào button "Edit"
        edit_button.click()
        time.sleep(5)
        driver.implicitly_wait(10)


# 7. Đóng trình duyệt sau khi hoàn thành kiểm tra
driver.quit()

df = pd.DataFrame(test_results)

# 8. Export the DataFrame to an Excel file
report_file = 'Feature2_test_report.xlsx'
df.to_excel(report_file, index=False)
print(f"Test report generated: {report_file}")