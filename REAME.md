# Swag Labs & Reqres API Automation Testing

โปรเจกต์ทดสอบอัตโนมัติ (Automation Testing) ครอบคลุมทั้งฝั่ง Web UI และ REST API
พัฒนาด้วย Python เพื่อจำลองการทดสอบสถานการณ์การใช้งานจริงของผู้ใช้

## Overview

โปรเจกต์นี้แบ่งเป็น 2 ส่วนหลัก:

### 1. UI Automation Test (`test_saucedemo_ui.py`)
ทดสอบขั้นตอนการสั่งซื้อสินค้าแบบ End-to-End บนเว็บไซต์ [Swag Labs](https://www.saucedemo.com/)
- Login เข้าสู่ระบบ
- ค้นหาและเพิ่มสินค้าลงตะกร้า (T-Shirt, Bike Light, Backpack)
- ลบสินค้าออกจากตะกร้า
- ดำเนินการ Checkout และกรอกข้อมูลผู้สั่งซื้อ
- ตรวจสอบความถูกต้องของราคารวมและภาษี (8%)
- ยืนยันหน้าจอสั่งซื้อสำเร็จ

### 2. API Automation Test (`test_reqres_api.py`)
ทดสอบ REST API บนเว็บไซต์ [Reqres](https://reqres.in/) ครอบคลุม 4 Method หลัก:
- **CREATE** (POST) — สร้างผู้ใช้ใหม่
- **SINGLE USER** (GET) — ดึงข้อมูลผู้ใช้รายบุคคล
- **UPDATE** (PUT) — แก้ไขข้อมูลผู้ใช้
- **DELETE** — ลบผู้ใช้

ทุก Test Case ตรวจสอบทั้ง Response Status Code และ Response Body ว่าตรงตาม Input ที่ส่งไป

## Tools & Technologies

| Component | Tool |
|---|---|
| Language | Python 3 |
| UI Testing | Selenium WebDriver |
| API Testing | Requests library |
| Test Framework | unittest |
| Configuration | JSON (แยก config ออกจาก logic เพื่อให้แก้ไข test data ได้ง่าย) |

## Project Structure├── test_saucedemo_ui.py # Test script สำหรับ UI Automation
├── test_reqres_api.py # Test script สำหรับ API Automation
├── ui_config.json # Configuration สำหรับ UI test (URL, keyword, test data)
├── api_config.json # Configuration สำหรับ API test (base URL, payload)
├── ui_test_cases.md # เอกสาร Test Case ฝั่ง UI
├── api_test_cases.md # เอกสาร Test Case ฝั่ง API
├── ui_test_results.txt # ผลการทดสอบ UI (auto-generated)
└── api_test_results.txt # ผลการทดสอบ API (auto-generated)

## How to Run

```bash
pip install selenium requests

# รันเทส UI
python test_saucedemo_ui.py

# รันเทส API
python test_reqres_api.py
```

ผลการทดสอบจะถูกบันทึกลงไฟล์ `.txt` ที่เกี่ยวข้องโดยอัตโนมัติหลังรันเสร็จ