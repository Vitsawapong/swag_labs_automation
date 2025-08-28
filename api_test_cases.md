Test Cases สำหรับ API จาก reqres.in
API: Create User (POST /api/users)
คำอธิบาย: ทดสอบการสร้างผู้ใช้ใหม่

Test Case ID: API-001-POST-CREATE

Pre-condition: ระบบ API ทำงานได้ปกติ, มี API Key ที่ถูกต้อง

Test Data:

    name: "morpheus"

    job: "leader"

Test Steps:

    1.ส่งคำขอ HTTP POST ไปยัง URL https://reqres.in/api/users

    2.แนบ JSON Payload ตาม Test Data

    3.แนบ Header x-api-key: reqres-free-v1

Expected Result:

    1.Response Status Code: 201 Created

    2.Response Body: ต้องมีฟิลด์ id และ createdAt และค่าของ name กับ job ต้องตรงกับที่ส่งไปใน Payload

    ตัวอย่าง Response Body: {"name": "morpheus", "job": "leader", "id": "...", "createdAt": "..."}

API: Get Single User (GET /api/users/{id})
คำอธิบาย: ทดสอบการดึงข้อมูลผู้ใช้คนเดียว

Test Case ID: API-002-GET-SINGLE

Pre-condition: ระบบ API ทำงานได้ปกติ, ผู้ใช้ ID 2 มีอยู่จริง, มี API Key ที่ถูกต้อง

Test Data:

    user_id: 2

Test Steps:

    1.ส่งคำขอ HTTP GET ไปยัง URL https://reqres.in/api/users/2

    2.แนบ Header x-api-key: reqres-free-v1

Expected Result:

    1.Response Status Code: 200 OK

    2.Response Body: ต้องมีฟิลด์ data ที่มี id: 2, email, first_name, last_name, avatar

    ตัวอย่าง Response Body: {"data": {"id": 2, "email": "janet.weaver@reqres.in", ...}, "support": {...}}

API: Update User (PUT /api/users/{id})
คำอธิบาย: ทดสอบการอัปเดตข้อมูลผู้ใช้ที่มีอยู่

Test Case ID: API-003-PUT-UPDATE

Pre-condition: ระบบ API ทำงานได้ปกติ, ผู้ใช้ ID 2 มีอยู่จริง, มี API Key ที่ถูกต้อง

Test Data:

    user_id: 2

    name: "morpheus"

    job: "zion resident"

Test Steps:

    1.ส่งคำขอ HTTP PUT ไปยัง URL https://reqres.in/api/users/2

    2.แนบ JSON Payload ตาม Test Data

    3.แนบ Header x-api-key: reqres-free-v1

Expected Result:

    1.Response Status Code: 200 OK

    2.Response Body: ต้องมีฟิลด์ updatedAt และค่าของ name กับ job ต้องตรงกับที่ส่งไปใน Payload

    ตัวอย่าง Response Body: {"name": "morpheus", "job": "zion resident", "updatedAt": "..."}

API: Delete User (DELETE /api/users/{id})
คำอธิบาย: ทดสอบการลบผู้ใช้ที่มีอยู่

Test Case ID: API-004-DELETE-USER

Pre-condition: ระบบ API ทำงานได้ปกติ, ผู้ใช้ ID 2 มีอยู่จริง, มี API Key ที่ถูกต้อง

Test Data:

    user_id: 2

Test Steps:

    1.ส่งคำขอ HTTP DELETE ไปยัง URL https://reqres.in/api/users/2

    2.แนบ Header x-api-key: reqres-free-v1

Expected Result:

    1.Response Status Code: 204 No Content

    2.Response Body: Response body ควรจะว่างเปล่า