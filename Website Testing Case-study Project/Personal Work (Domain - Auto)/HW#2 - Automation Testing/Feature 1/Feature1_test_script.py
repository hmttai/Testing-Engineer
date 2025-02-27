from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.service import Service
from openpyxl.workbook import Workbook
import time
import csv
import pandas as pd
import os

# 1. Kết nối và truy cập trang web
service = Service(executable_path=r'./msedgedriver.exe')
driver = webdriver.Edge(service = service)
driver.get("http://localhost:8080/orangehrm-4.5/symfony/web/index.php/admin/saveSystemUser")

test_results = []


# Đợi 2 giây trước khi thao tác với phần tử
time.sleep(2)

# 2. Đăng nhập vào trang web
username_field = driver.find_element(By.ID, 'txtUsername')
username_field.send_keys("Admin")

password_field = driver.find_element(By.ID, "txtPassword")
password_field.send_keys("suViet99.000")

password_field.send_keys(Keys.RETURN)

time.sleep(2)
# 3. Đọc dữ liệu từ file CSV
with open('Feature1_test_data.csv', newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        en = row['Employee Name']
        un = row['Username']
        p = row['Password']
        cp = row['Confirm Password']
        er = row['Expected Result']
        print([en, un, p, cp])
        
        empName = driver.find_element(By.ID, "systemUser_employeeName_empName")
        empName.clear()
        empName.send_keys(en)

        userName = driver.find_element(By.ID, "systemUser_userName")
        userName.clear()
        userName.send_keys(un)

        password = driver.find_element(By.ID, "systemUser_password")
        password.clear()
        password.send_keys(p)

        confirmPassword = driver.find_element(By.ID, "systemUser_confirmPassword")
        confirmPassword.clear()
        confirmPassword.send_keys(cp)

        save_button = driver.find_element(By.ID, "btnSave")
        save_button.click()
                
        time.sleep(10)
        driver.implicitly_wait(10)  

        # 4. Kiểm tra trạng thái URL sau khi thêm thành công
        target_url = "http://localhost:8080/orangehrm-4.5/symfony/web/index.php/admin/viewSystemUsers"
        if driver.current_url == target_url:
            print("Thao tác thêm người dùng thành công.\n")
            test_results.append({'Employee Name': en, 'Username': un, 'Password': p, 'Confirm Password': cp,'Expected Result': er, 'Actual Result': 'Passed'})
        else:
            print("Thao tác thêm người dùng thất bại.\n")
            test_results.append({'Employee Name': en, 'Username': un, 'Password': p, 'Confirm Password': cp, 'Expected Result': er, 'Actual Result': 'Failed'})
        
        driver.get("http://localhost:8080/orangehrm-4.5/symfony/web/index.php/admin/saveSystemUser")
        time.sleep(5)
        driver.implicitly_wait(10)


# 5. Đóng trình duyệt sau khi hoàn thành kiểm tra
driver.quit()

df = pd.DataFrame(test_results)

# 6. Xuất ra file report
report_file = 'Feature1_test_report.xlsx'
df.to_excel(report_file, index=False)
print(f"Test report generated: {report_file}")