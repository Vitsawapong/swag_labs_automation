# Swag Labs & Reqres API Automation Testing

โปรเจกต์ทดสอบอัตโนมัติ (Automation Testing) ครอบคลุมทั้ง Web UI และ REST API พัฒนาด้วย Python เพื่อจำลองสถานการณ์ใช้งานจริงของผู้ใช้

## Overview

### 1. UI Automation Test (`test_saucedemo_ui.py`)
ทดสอบขั้นตอนสั่งซื้อสินค้าแบบ End-to-End บนเว็บไซต์ [Swag Labs](https://www.saucedemo.com/)

- Login เข้าสู่ระบบ
- เพิ่มสินค้าลงตะกร้า (T-Shirt, Bike Light, Backpack)
- ลบสินค้าออกจากตะกร้า
- Checkout และกรอกข้อมูลผู้สั่งซื้อ
- ตรวจสอบราคารวมและภาษี 8%
- ยืนยันหน้าสั่งซื้อสำเร็จ (Thank you)

### 2. API Automation Test (`test_reqres_api.py`)
ทดสอบ REST API บน [Reqres](https://reqres.in/) ครอบคลุม 4 Method

- **CREATE** (POST): สร้างผู้ใช้ใหม่
- **SINGLE USER** (GET): ดึงข้อมูลผู้ใช้
- **UPDATE** (PUT): แก้ไขข้อมูลผู้ใช้
- **DELETE**: ลบผู้ใช้

ทุก Test Case ตรวจสอบทั้ง Status Code และ Response Body

## Tools & Technologies

| Component | Tool |
|---|---|
| Language | Python 3 |
| UI Testing | Selenium WebDriver |
| API Testing | Requests library |
| Test Framework | unittest |
| Configuration | JSON (แยก config ออกจากโค้ด แก้ test data ได้ง่าย) |

## Project Structure

```
swag_labs_automation/
├── test_saucedemo_ui.py     # Test script: UI Automation
├── test_reqres_api.py       # Test script: API Automation
├── ui_config.json           # Config ฝั่ง UI (URL, keyword, test data)
├── api_config.json          # Config ฝั่ง API (base URL, payload)
├── ui_test_cases.md         # เอกสาร Test Case ฝั่ง UI
├── api_test_cases.md        # เอกสาร Test Case ฝั่ง API
├── ui_test_results.txt      # ผลทดสอบ UI (สร้างอัตโนมัติ)
└── api_test_results.txt     # ผลทดสอบ API (สร้างอัตโนมัติ)
```

## How to Run

1. ติดตั้ง Python 3 และเบราว์เซอร์ [Chrome/Edge]
2. เปิด Command Prompt แล้วเข้าไปที่โฟลเดอร์โปรเจกต์ (`cd` ไปยังโฟลเดอร์นี้ก่อน)
3. ติดตั้งไลบรารีและรัน

```
pip install selenium requests

python test_saucedemo_ui.py
python test_reqres_api.py
```

ผลการทดสอบจะถูกบันทึกลงไฟล์ `.txt` อัตโนมัติหลังรันเสร็จ

หมายเหตุ: ใน `ui_config.json` ใช้ key ชื่อ `username` และ `password`

## Known Limitations
- ยังไม่มี negative test, edge case และ performance check
- ทดสอบบนเว็บทดลอง (saucedemo.com, reqres.in) เพื่อการเรียนรู้

## Author
Vitsawapong Puaphan | vitsawapong.puaphan@gmail.com
