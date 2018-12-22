#CS683 : Parallel Algorithm Project
Term Project 1st @2018

	Thailand political party popular by Word counter from Website
		- PyThon
		- Use AsyncIO to get data from URL
		- Procress Data
			- Word count

		1. อ่านรายชื่อพรรคการเมืองจาก json file มาใช้เป็นข้อมูลตั้งต้น ซึ่งข้อมูลจะประกอบไปด้วย -> บันทึกข้อมูลนี้ไว้ใน redis server ด้วย
			- รหัสพรรค : เก็บรูป logo ของพรรคใน [party] โดยใช้ชื่อเป็นรหัสพรรค
			- ชื่อภาษาไทย
			- ชื่อภาษาอังกฤษ
			- ชื่อย่อ
			- วันที่จัดตั้ง
			- หัวหน้าพรรค
			*- popular : เก็บจำนวนครั้งที่พบชื่อพรรค
			*- counter : เก็บจำนวน url ที่ค้นหา
			*- update  : เก็บข้มูลเวลาที่ update ข้อมูลครั้งล่าสุด

		2. นำรายชื่อทั้งหมดจาก json ไปค้นหาใน google.co.th แล้วเอา link ทั้งหมดในหน้าแรกของผลการค้นหา มาประมวลผล
			- ค้นหา link ทั้งหมดที่มีใน body แล้วจัดเก็บข้อมูลลง redis server : url link, visit status = 0
		
		3. นำข้อมูล link ทั้งหมดที่ได้มาจากขั้นตอนที่ 2 มา call เพื่อ visit แล้วนำ body มาประมวลผลข้อมูล ดังนี้
			- ค้นหาชื่อพรรคการเมืองใน body และทำการนับจำนวน update ค่าข้อมูล popular ของแต่ละพรรคใน redis server
			- update ค่าใน redis server ว่า visit status = 1
			- update ค่าใน 
			- ค้นหา link ทั้งหมดที่มีใน body แล้วจัดเก็บข้อมูลลง redis server : url link, visit status = 0

		4. นำข้อมูล link ทั้งหมดที่มีใน redis server มาประมวลแบบในข้อ 3 จนกว่าไม่มีข้อมูลที่ visit status = 0 เหลือให้ประมวลผล   
		   หรือประมวลผลครบ 1,000 รายการแล้ว counter > 1,000 ให้หยุด

		5. update ค่า counter ที่เก็บใน redis server ลงใน json file เมื่อประมวลผลเสร็จทั้งหมดแล้ว