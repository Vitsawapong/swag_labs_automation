import unittest
import json
import requests
import os
import time

# โหลดการตั้งค่าจากไฟล์ config.json
CONFIG_FILE = 'api_config.json'
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"'{CONFIG_FILE}' ไม่พบ. กรุณาสร้างไฟล์ config.json ตามตัวอย่างที่ให้ไว้.")

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config_data = json.load(f)

# กำหนดชื่อไฟล์สำหรับบันทึกผลการทดสอบ
API_TEST_RESULTS_FILE = 'api_test_results.txt'

class ReqresAPITest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ตั้งค่า Base URL, Headers และ Test Data ที่ใช้ร่วมกันสำหรับทุก Test Case"""
        cls.base_url = config_data['base_url']
        cls.headers = config_data['headers']
        cls.create_user_data = config_data['user_data']['create_user']
        cls.update_user_data = config_data['user_data']['update_user']
        cls.specific_user_id = config_data['user_data']['specific_user_id']
        cls.test_log = []

    def setUp(self):
        self.current_test_log = []

    def tearDown(self):
        test_method_name = self._testMethodName
        self.test_log.append(f"\n--- {test_method_name} ---")
        self.test_log.extend(self.current_test_log)
        self.test_log.append(f"--- จบ {test_method_name} ---\n")

    @classmethod
    def tearDownClass(cls):
        """บันทึก log ทั้งหมดลงไฟล์เมื่อ Test Class ทำงานเสร็จสิ้น"""
        with open(API_TEST_RESULTS_FILE, 'a', encoding='utf-8') as f:
            f.write("\n" + "#"*60 + "\n")
            f.write(f"API Test Run on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("API Test Results for reqres.in\n")
            f.write("\n".join(cls.test_log))
            f.write("\n" + "#"*60 + "\n")

    def log_step(self, message):
        print(message)
        self.current_test_log.append(message)

    def test_01_create_user(self):
        """
        API-001-POST-CREATE: ทดสอบการสร้างผู้ใช้ใหม่ (POST)
        """
        self.log_step("กำลังทดสอบ: API-001-POST-CREATE")
        endpoint = self.base_url
        payload = self.create_user_data

        self.log_step(f"   -> ส่ง POST request ไปยัง: {endpoint}")
        self.log_step(f"   -> Payload: {json.dumps(payload)}")
        response = requests.post(endpoint, json=payload, headers=self.headers)

        self.log_step(f"   <- Response Status Code: {response.status_code}")
        self.log_step(f"   <- Response Body: {response.text}")

        self.assertEqual(response.status_code, 201, f"   ✗ สถานะโค้ดไม่ถูกต้อง. คาดหวัง 201, ได้รับ {response.status_code}")
        self.log_step("   ✓ สถานะโค้ด 201 Created ถูกต้อง")

        response_data = response.json()
        self.assertIn("id", response_data, "   ✗ Response ไม่มีฟิลด์ 'id'")
        self.assertIn("createdAt", response_data, "   ✗ Response ไม่มีฟิลด์ 'createdAt'")
        self.assertEqual(response_data["name"], payload["name"], f"   ✗ ชื่อไม่ตรงกัน. คาดหวัง {payload['name']}, ได้รับ {response_data['name']}")
        self.assertEqual(response_data["job"], payload["job"], f"   ✗ ตำแหน่งไม่ตรงกัน. คาดหวัง {payload['job']}, ได้รับ {response_data['job']}")
        self.log_step("   ✓ Response body ถูกต้องและมีข้อมูลที่จำเป็น")
        self.log_step("API-001-POST-CREATE ทดสอบผ่าน")

    def test_02_get_single_user(self):
        """
        API-002-GET-SINGLE: ทดสอบการดึงข้อมูลผู้ใช้คนเดียว (GET)
        """
        self.log_step("กำลังทดสอบ: API-002-GET-SINGLE")
        endpoint = f"{self.base_url}/{self.specific_user_id}"

        self.log_step(f"   -> ส่ง GET request ไปยัง: {endpoint}")
        response = requests.get(endpoint, headers=self.headers)

        self.log_step(f"   <- Response Status Code: {response.status_code}")
        self.log_step(f"   <- Response Body: {response.text}")

        self.assertEqual(response.status_code, 200, f"   ✗ สถานะโค้ดไม่ถูกต้อง. คาดหวัง 200, ได้รับ {response.status_code}")
        self.log_step("   ✓ สถานะโค้ด 200 OK ถูกต้อง")

        response_data = response.json()["data"]
        self.assertEqual(response_data["id"], self.specific_user_id, f"   ✗ ID ผู้ใช้ไม่ตรงกัน. คาดหวัง {self.specific_user_id}, ได้รับ {response_data['id']}")
        self.assertIn("email", response_data, "   ✗ Response ไม่มีฟิลด์ 'email'")
        self.assertIn("first_name", response_data, "   ✗ Response ไม่มีฟิลด์ 'first_name'")
        self.log_step(f"   ✓ ข้อมูลผู้ใช้ ID {self.specific_user_id} ถูกต้อง")
        self.log_step("API-002-GET-SINGLE ทดสอบผ่าน")

    def test_03_update_user(self):
        """
        API-003-PUT-UPDATE: ทดสอบการอัปเดตข้อมูลผู้ใช้ที่มีอยู่ (PUT)
        """
        self.log_step("กำลังทดสอบ: API-003-PUT-UPDATE")
        endpoint = f"{self.base_url}/{self.specific_user_id}"
        payload = self.update_user_data

        self.log_step(f"   -> ส่ง PUT request ไปยัง: {endpoint}")
        self.log_step(f"   -> Payload: {json.dumps(payload)}")
        response = requests.put(endpoint, json=payload, headers=self.headers)

        self.log_step(f"   <- Response Status Code: {response.status_code}")
        self.log_step(f"   <- Response Body: {response.text}")

        self.assertEqual(response.status_code, 200, f"   ✗ สถานะโค้ดไม่ถูกต้อง. คาดหวัง 200, ได้รับ {response.status_code}")
        self.log_step("   ✓ สถานะโค้ด 200 OK ถูกต้อง")

        response_data = response.json()
        self.assertIn("updatedAt", response_data, "   ✗ Response ไม่มีฟิลด์ 'updatedAt'")
        self.assertEqual(response_data["name"], payload["name"], f"   ✗ ชื่อไม่ตรงกัน. คาดหวัง {payload['name']}, ได้รับ {response_data['name']}")
        self.assertEqual(response_data["job"], payload["job"], f"   ✗ ตำแหน่งไม่ตรงกัน. คาดหวัง {payload['job']}, ได้รับ {response_data['job']}")
        self.log_step("   ✓ Response body ถูกต้องและมีข้อมูลที่อัปเดตแล้ว")
        self.log_step("API-003-PUT-UPDATE ทดสอบผ่าน")

    def test_04_delete_user(self):
        """
        API-004-DELETE-USER: ทดสอบการลบผู้ใช้ (DELETE)
        """
        self.log_step("กำลังทดสอบ: API-004-DELETE-USER")
        endpoint = f"{self.base_url}/{self.specific_user_id}"

        self.log_step(f"   -> ส่ง DELETE request ไปยัง: {endpoint}")
        response = requests.delete(endpoint, headers=self.headers)

        self.log_step(f"   <- Response Status Code: {response.status_code}")
        self.log_step(f"   <- Response Body: '{response.text}' (ควรจะว่างเปล่า)")

        self.assertEqual(response.status_code, 204, f"   ✗ สถานะโค้ดไม่ถูกต้อง. คาดหวัง 204, ได้รับ {response.status_code}")
        self.log_step("   ✓ สถานะโค้ด 204 No Content ถูกต้อง")

        self.assertEqual(response.text, "", "   ✗ Response body ไม่ว่างเปล่า")
        self.log_step("   ✓ Response body ว่างเปล่าตามที่คาดหวัง")
        self.log_step("API-004-DELETE-USER ทดสอบผ่าน")

if __name__ == '__main__':
    if os.path.exists(API_TEST_RESULTS_FILE):
        os.remove(API_TEST_RESULTS_FILE)
    unittest.main()