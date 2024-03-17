
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

lakNuayReading = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
lakOtherReading = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
lakSibReading = ["", "", "ยี่", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
lakNuaySibReading = ["", "เอ็ด", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
lakReading = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

number = input("Enter number: ")
if int(number) < 0 or int(number) > 9999999:
    raise Exception("Sorry, numbers are out of range")
reading = ""
for i in range(len(number)):
    numberStr = str(number)
    numberAtI = int(numberStr[i])
    indexAtI = len(numberStr) - i - 1
    if len(numberStr) == 1:
        reading += lakNuayReading[numberAtI]
        break
    elif indexAtI == 1:
        reading += lakSibReading[numberAtI]
    elif indexAtI == 0 and numberStr[i-1] != 0:
        reading += lakNuaySibReading[numberAtI]
    else:
        reading += lakOtherReading[numberAtI]
        
    if numberAtI != 0 or indexAtI == 6:
        reading += lakReading[indexAtI]

print(reading)