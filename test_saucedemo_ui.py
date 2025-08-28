import unittest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os

# โหลดการตั้งค่าจากไฟล์ config.json
CONFIG_FILE = 'ui_config.json'
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"'{CONFIG_FILE}' ไม่พบ. กรุณาสร้างไฟล์ config.json ตามตัวอย่างที่ให้ไว้.")

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config_data = json.load(f)

# กำหนดชื่อไฟล์สำหรับบันทึกผลการทดสอบ
TEST_RESULTS_FILE = 'ui_test_results.txt'

class SwagLabsUITest(unittest.TestCase):

    def setUp(self):
        """ตั้งค่า WebDriver และเปิดเบราว์เซอร์ก่อนเริ่มแต่ละ Test Case"""
        self.driver = webdriver.Edge() # หรือ webdriver.Firefox(), webdriver.Edge()
        self.driver.maximize_window()
        self.driver.get(config_data['web_url'])
        self.wait = WebDriverWait(self.driver, 10) # ตั้งค่าการรอสูงสุด 10 วินาที
        self.test_log = [] # ใช้เก็บ log สำหรับ Test Case นี้

    def tearDown(self):
        """ปิดเบราว์เซอร์เมื่อทดสอบแต่ละ Test Case เสร็จสิ้น"""
        self.driver.quit()
        # บันทึก log ลงไฟล์เมื่อ Test Case เสร็จสิ้น
        with open(TEST_RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write("\n" + "="*50 + "\n")
            f.write(f"Test Run on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Test: test_purchase_workflow\n")
            f.write("\n".join(self.test_log))
            f.write("\n" + "="*50 + "\n")

    def log_step(self, message):
        """ฟังก์ชันสำหรับบันทึกขั้นตอนและผลลัพธ์ลงใน log"""
        print(message)
        self.test_log.append(message)

    def test_purchase_workflow(self):
        """
        Test Case หลัก: ทดสอบขั้นตอนการ Login, เลือกสินค้า, ลบสินค้า, Checkout และยืนยันการสั่งซื้อ
        """
        self.log_step("--- เริ่มต้นการทดสอบขั้นตอนการสั่งซื้อสินค้า ---")

        # ขั้นตอนที่ 1: เข้าสู่หน้าเว็บและทำการ Login
        self.log_step("1. เข้าสู่หน้าเว็บและทำการ Login...")
        try:
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, config_data['keywords']['login_page']['username_input'])))
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, config_data['keywords']['login_page']['password_input'])))
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, config_data['keywords']['login_page']['login_button'])))

            username_field.send_keys(config_data['users']['standard_user'])
            password_field.send_keys(config_data['users']['locked_out_user']) # Password ก็คือ standard_user ตามโจทย์
            login_button.click()

            self.wait.until(EC.url_contains("inventory.html"))
            self.log_step("   ✓ เข้าสู่ระบบสำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ การเข้าสู่ระบบล้มเหลว: {e}")
        time.sleep(1) # เพื่อให้เห็นการเปลี่ยนแปลงบนหน้าจอ

        # ขั้นตอนที่ 2: เลือกหาซื้อสินค้า (T-Shirt, Flashlight, Backpack) และเพิ่มลงในรถเข็น
        self.log_step("2. เลือกหาซื้อสินค้าและเพิ่มลงในรถเข็น...")
        products_added_count = 0
        products_not_found = []
        for product in config_data['products_to_buy']:
            product_name = product['name']
            add_to_cart_id = product['add_id']
            try:
                add_button = self.wait.until(EC.element_to_be_clickable((By.ID, add_to_cart_id)))
                add_button.click()
                products_added_count += 1
                self.log_step(f"   ✓ หยิบสินค้า '{product_name}' ใส่รถเข็นสำเร็จ")
            except (NoSuchElementException, TimeoutException):
                products_not_found.append(product_name)
                self.log_step(f"   ✗ ไม่พบสินค้า '{product_name}' หรือปุ่ม 'Add to cart' ไม่พร้อมใช้งาน")
            time.sleep(0.5) # เพื่อให้เห็นการเปลี่ยนแปลงบนหน้าจอ

        if products_not_found:
            self.log_step(f"   ! สินค้าที่ไม่พบ: {', '.join(products_not_found)}. โปรแกรมดำเนินการต่อ.")
        self.assertEqual(products_added_count, len(config_data['products_to_buy']) - len(products_not_found),
                         f"จำนวนสินค้าที่เพิ่มไม่ตรงกับที่คาดไว้: {products_added_count} จาก {len(config_data['products_to_buy']) - len(products_not_found)} ชิ้นที่ควรจะหาเจอ")
        self.log_step(f"   ✓ เพิ่มสินค้าที่พบ {products_added_count} ชิ้นลงในรถเข็น")
        time.sleep(1)

        # คลิกไปที่ตะกร้าสินค้า
        self.log_step("   -> ไปยังหน้าตะกร้าสินค้า...")
        try:
            shopping_cart = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, config_data['keywords']['inventory_page']['shopping_cart_link_class'])))
            shopping_cart.click()
            self.wait.until(EC.url_contains("cart.html"))
            self.log_step("   ✓ เข้าสู่หน้าตะกร้าสินค้าสำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่สามารถไปยังหน้าตะกร้าสินค้าได้: {e}")
        time.sleep(1)

        # ขั้นตอนที่ 3: ลูกค้าตัดสินใจคืนสินค้า Backpack
        self.log_step("3. ดำเนินการคืนสินค้า Backpack...")
        try:
            # ค้นหาปุ่ม Remove สำหรับ Backpack
            backpack_remove_id = config_data['products_to_buy'][2]['remove_id'] # Backpack เป็นสินค้าตัวที่ 3 ใน list
            remove_button = self.wait.until(EC.element_to_be_clickable((By.ID, backpack_remove_id)))
            remove_button.click()
            self.log_step("   ✓ ลบสินค้า 'Sauce Labs Backpack' ออกจากรถเข็นสำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่สามารถลบสินค้า 'Sauce Labs Backpack' ได้: {e}")
        time.sleep(1)

        # ตรวจสอบสินค้าที่เหลือในตะกร้า (ควรจะมี T-Shirt และ Flashlight)
        self.log_step("   -> ตรวจสอบสินค้าที่เหลือในตะกร้า...")
        remaining_products = ["Sauce Labs Bolt T-Shirt", "Sauce Labs Bike Light"]
        for product_name in remaining_products:
            try:
                # ตรวจสอบว่ามีชื่อสินค้าปรากฏอยู่ในตะกร้า
                self.wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@class='inventory_item_name' and text()='{product_name}']")))
                self.log_step(f"      ✓ พบสินค้า '{product_name}' ในตะกร้า")
            except (NoSuchElementException, TimeoutException):
                self.fail(f"   ✗ ไม่พบสินค้า '{product_name}' ในตะกร้าหลังการลบ Backpack")
        self.log_step("   ✓ สินค้าในตะกร้าถูกต้องครบถ้วน")
        time.sleep(1)

        # คลิกปุ่ม Checkout
        self.log_step("   -> ดำเนินการ Checkout...")
        try:
            checkout_button = self.wait.until(EC.element_to_be_clickable((By.ID, config_data['keywords']['cart_page']['checkout_button'])))
            checkout_button.click()
            self.wait.until(EC.url_contains("checkout-step-one.html"))
            self.log_step("   ✓ เข้าสู่หน้าข้อมูลผู้สั่งซื้อ (Checkout Step One) สำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่สามารถคลิกปุ่ม Checkout ได้: {e}")
        time.sleep(1)

        # ขั้นตอนที่ 4: กรอกข้อมูลผู้สั่งซื้อ จากนั้นกดปุ่ม Continue
        self.log_step("4. กรอกข้อมูลผู้สั่งซื้อ...")
        try:
            first_name_field = self.wait.until(EC.presence_of_element_located((By.ID, config_data['keywords']['checkout_step_one_page']['first_name_input'])))
            last_name_field = self.wait.until(EC.presence_of_element_located((By.ID, config_data['keywords']['checkout_step_one_page']['last_name_input'])))
            zip_code_field = self.wait.until(EC.presence_of_element_located((By.ID, config_data['keywords']['checkout_step_one_page']['zip_postal_code_input'])))
            continue_button = self.wait.until(EC.element_to_be_clickable((By.ID, config_data['keywords']['checkout_step_one_page']['continue_button'])))

            first_name_field.send_keys(config_data['checkout_info']['first_name'])
            last_name_field.send_keys(config_data['checkout_info']['last_name'])
            zip_code_field.send_keys(config_data['checkout_info']['zip_code'])
            continue_button.click()

            self.wait.until(EC.url_contains("checkout-step-two.html"))
            self.log_step("   ✓ กรอกข้อมูลผู้สั่งซื้อและดำเนินการต่อสำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ การกรอกข้อมูลผู้สั่งซื้อล้มเหลว: {e}")
        time.sleep(1)

        # ขั้นตอนที่ 5: ตรวจสอบรายการสินค้าครั้งสุดท้าย และราคารวม
        self.log_step("5. ตรวจสอบรายการสินค้าและราคารวม...")
        try:
            # ดึงค่า Item Total, Tax และ Total จากหน้าเว็บ
            item_total_text = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config_data['keywords']['checkout_step_two_page']['item_total_label_class']))).text
            tax_text = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config_data['keywords']['checkout_step_two_page']['tax_label_class']))).text
            total_text = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config_data['keywords']['checkout_step_two_page']['total_label_class']))).text

            # แปลงค่าเป็นตัวเลข (โดยตัด "Item total: $" และ "Tax: $" และ "Total: $")
            item_total = float(item_total_text.replace("Item total: $", ""))
            tax_amount = float(tax_text.replace("Tax: $", ""))
            total_amount = float(total_text.replace("Total: $", ""))

            # คำนวณภาษีที่คาดหวัง (8%)
            expected_tax = round(item_total * 0.08, 2)
            expected_total = round(item_total + expected_tax, 2)

            # ตรวจสอบความถูกต้อง
            self.assertAlmostEqual(tax_amount, expected_tax, places=2, msg=f"   ✗ ภาษีไม่ถูกต้อง: คาดหวัง {expected_tax}, ได้รับ {tax_amount}")
            self.assertAlmostEqual(total_amount, expected_total, places=2, msg=f"   ✗ ราคารวมไม่ถูกต้อง: คาดหวัง {expected_total}, ได้รับ {total_amount}")
            self.log_step(f"   ✓ ราคารวมของสินค้า ({item_total}), ภาษี ({tax_amount}) และราคารวมทั้งหมด ({total_amount}) ถูกต้อง")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่สามารถตรวจสอบราคารวมได้: {e}")
        time.sleep(1)

        # คลิกปุ่ม Finish
        self.log_step("   -> คลิกปุ่ม Finish เพื่อยืนยันการสั่งซื้อ...")
        try:
            finish_button = self.wait.until(EC.element_to_be_clickable((By.ID, config_data['keywords']['checkout_step_two_page']['finish_button'])))
            finish_button.click()
            self.wait.until(EC.url_contains("checkout-complete.html"))
            self.log_step("   ✓ สั่งซื้อสำเร็จ")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่สามารถคลิกปุ่ม Finish ได้: {e}")
        time.sleep(1)

        # ขั้นตอนที่ 6: ตรวจสอบหน้าจอ "Thank you for your order!"
        self.log_step("6. ตรวจสอบหน้าจอ 'Thank you for your order!'...")
        try:
            thank_you_header = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, config_data['keywords']['checkout_complete_page']['thank_you_header'])))
            self.assertIn("Thank you for your order!", thank_you_header.text)
            self.log_step("   ✓ พบข้อความ 'Thank you for your order!'")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"   ✗ ไม่พบข้อความ 'Thank you for your order!': {e}")

        self.log_step("--- สิ้นสุดการทดสอบขั้นตอนการสั่งซื้อสินค้า ---")

if __name__ == '__main__':
    # ล้างไฟล์ log เก่าก่อนเริ่มรัน Test Case ใหม่
    if os.path.exists(TEST_RESULTS_FILE):
        os.remove(TEST_RESULTS_FILE)
    unittest.main()

