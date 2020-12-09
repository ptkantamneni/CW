TRUNCATE TABLE event;
TRUNCATE TABLE relationship;
TRUNCATE TABLE "user";

INSERT INTO "public"."user"("id","firstName","lastName","email","address","age","testResult","testDate","hasSymptoms","symptomsOnSetDate","password")
VALUES
(1,E'David',E'Nguyen',E'david@clari.com',E'1655 Tully Rd, San Jose, CA 95122',21,NULL,NULL,TRUE,E'2020-12-05',E'123'),
(2,E'Phani',E'Kantamneni',E'phani@clari.com',E'2525 S King Rd, San Jose, CA 95122',21,E'FALSE',E'2020-11-25',FALSE,NULL,E'123'),
(3,E'Divya',E'Narasimhan',E'divya@clari.com',E'1290 Tully Rd suite 50, San Jose, CA 95122',21,NULL,NULL,FALSE,NULL,E'123'),
(4,E'Aditya',E'Varkhedi',E'aditya@clari.com',E'2055 Summerside Dr, San Jose, CA 95122',21,NULL,NULL,FALSE,NULL,E'123'),
(5,E'Tony',E'Nguyen',E'tony@gmail.com',E'1710 Tully Rd, San Jose, CA 95122',33,NULL,NULL,FALSE,NULL,E'123'),
(6,E'Lisa',E'Nguyen',E'lisa@gmail.com',E'1855 Lucretia Ave, San Jose, CA 95122',65,NULL,NULL,FALSE,NULL,E'123'),
(7,E'Tina',E'Nguyen',E'tina@gmail.com',E'2201 Senter Rd, San Jose, CA 95112',32,NULL,NULL,FALSE,NULL,E'123');


INSERT INTO "public"."event"("id","placeName","address","numPeople","socialDistanceRating","maskComplianceRating","openSpace","riskScore","createdById","checkInDate","checkOutDate","updatedDate")
VALUES
(1,E'Walmart',E'777 Story Rd, San Jose, CA 95122',5,2,5,FALSE,3.2,1,E'2020-12-01 01:00:00',E'2020-12-01 02:00:00',E'2020-12-01 01:00:00'),
(2,E'Dennys',E'2401 Lanai Ave, San Jose, CA 95122',2,4,3,FALSE,2.9,1,E'2020-12-01 02:00:00',E'2020-12-01 03:00:00',E'2020-12-01 02:00:00'),
(3,E'Target',E'2161 Monterey Rd, San Jose, CA 95125',4,3,5,FALSE,3.3,1,E'2020-11-25 02:00:00',E'2020-11-25 04:00:00',E'2020-11-25 02:00:00'),
(4,E'Walmart',E'777 Story Rd, San Jose, CA 95122',5,3,5,FALSE,3.1,2,E'2020-12-01 01:00:00',E'2020-12-01 02:00:00',E'2020-12-01 01:00:00'),
(5,E'Walmart',E'777 Story Rd, San Jose, CA 95122',5,3,5,FALSE,3.1,3,E'2020-12-01 01:00:00',E'2020-12-01 02:00:00',E'2020-12-01 01:00:00'),
(6,E'Walmart',E'777 Story Rd, San Jose, CA 95122',5,3,5,FALSE,3.1,4,E'2020-12-01 01:00:00',E'2020-12-01 02:00:00',E'2020-12-01 01:00:00');

INSERT INTO "public"."relationship"("id","userId","friendId","relationshipType")
VALUES
(1,1,2,E'friend'),
(2,2,1,E'friend'),
(3,1,3,E'friend'),
(4,1,4,E'friend'),
(5,1,5,E'family'),
(6,1,6,E'family'),
(7,1,7,E'family'),
(8,3,1,E'friend'),
(9,4,1,E'friend');
