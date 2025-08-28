Test Cases สำหรับ Automated UI Test (SauceDemo)
TC-UI-001: Login และเลือกสินค้า
คำอธิบาย: ทดสอบขั้นตอนการล็อกอินและเพิ่มสินค้าที่กำหนดลงในรถเข็น

Pre-condition: ผู้ใช้มีข้อมูลล็อกอินที่ถูกต้องและเว็บไซต์ทำงานปกติ

Test Steps:

    1.เข้าสู่หน้าเว็บ https://www.saucedemo.com/

    2.กรอก Username "standard_user" และ Password "secret_sauce"

    3.กดปุ่ม Login

    4.เพิ่มสินค้า "Sauce Labs Bolt T-Shirt" และ "Sauce Labs Bike Light" ลงในรถเข็น

Expected Result:

    1.เข้าสู่หน้า inventory.html สำเร็จ

    2.สินค้าทั้งสองรายการถูกเพิ่มลงในรถเข็นและแสดงจำนวน (2) ที่ไอคอนรถเข็น

TC-UI-002: การแก้ไขรถเข็นและ Checkout
คำอธิบาย: ทดสอบการลบสินค้าออกจากรถเข็นและดำเนินการต่อเพื่อ Checkout

Pre-condition: มีสินค้าในรถเข็นอย่างน้อย 2 ชิ้น

Test Steps:

    1.คลิกที่ไอคอนรถเข็น

    2.กดปุ่ม "Remove" สำหรับสินค้า "Sauce Labs Bolt T-Shirt"

    3.กดปุ่ม "Checkout" และกรอกข้อมูลผู้ใช้ (Test, User, 10110)

Expected Result:

    1.สินค้าที่ถูกลบหายไปจากรถเข็น

    2.สามารถดำเนินการไปหน้า Checkout ได้

TC-UI-003: การตรวจสอบราคาและการยืนยันคำสั่งซื้อ
คำอธิบาย: ทดสอบการคำนวณราคาและยืนยันการสั่งซื้อจนสำเร็จ

Pre-condition: ดำเนินการมาถึงหน้า Overview ก่อนกดยืนยัน

Test Steps:

    1.ตรวจสอบราคา "Item Total"

    2.ตรวจสอบค่า "Tax" (8% ของ Item Total)

    3.ตรวจสอบค่า "Total" (Item Total + Tax)

    4.กดปุ่ม "Finish"

Expected Result:

    1.ค่าราคารวมและภาษีที่แสดงบนเว็บถูกต้องตามการคำนวณ

    2.หน้าจอแสดงข้อความ "Thank you for your order!"