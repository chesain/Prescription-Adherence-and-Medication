DROP SCHEMA IF EXISTS MEDICATION_SCHEMA;

CREATE SCHEMA MEDICATION_SCHEMA;
USE MEDICATION_SCHEMA;

CREATE TABLE HOSPITAL (
	Hospital_ID INT NOT NULL,
    H_Name VARCHAR(50),
    H_Address VARCHAR(255),
    
    PRIMARY KEY(Hospital_ID)
    );
    
    
CREATE TABLE MEDICATIONS (
	Med_ID INT NOT NULL,
    Med_Name VARCHAR(75),
    
    PRIMARY KEY(Med_ID)
    );


CREATE TABLE DOCTOR (
	Doc_ID INT NOT NULL,
    D_Fname VARCHAR(255),
    D_Lname VARCHAR(255),
    
    PRIMARY KEY(Doc_ID)
    );

CREATE TABLE PATIENT (
	Patient_ID INT NOT NULL,
    Fname VARCHAR(100), 
    Lname VARCHAR(100),
    Birthdate DATE,
    Height DECIMAL(4, 2),
    Weight DECIMAL(8, 2),
    Address VARCHAR(255),
    Hospital_ID INT,
    
    PRIMARY KEY(Patient_ID),
    FOREIGN KEY(Hospital_ID) REFERENCES HOSPITAL(Hospital_ID)
    );
    
CREATE TABLE PHONE_NUMBERS (
	Patient_ID INT NOT NULL,
    Patient_number BIGINT NOT NULL,
    
    PRIMARY KEY(Patient_number),
    FOREIGN KEY(Patient_ID) REFERENCES PATIENT(Patient_ID)
    );
    

CREATE TABLE PATIENT_PRESCRIPTIONS (
	PR_ID VARCHAR(10) NOT NULL,
    Patient_ID INT NOT NULL,
    Med_ID INT NOT NULL,
    
    PRIMARY KEY(PR_ID),
    FOREIGN KEY(Patient_ID) REFERENCES PATIENT(Patient_ID),
    FOREIGN KEY(Med_ID) REFERENCES MEDICATIONS(Med_ID)
    );

CREATE TABLE REFILL_INFO (
	Refill_ID INT NOT NULL AUTO_INCREMENT,
    PR_ID VARCHAR(10) NOT NULL,
    Refill_Date DATE,
    Doc_ID INT NOT NULL,
    Dosage INT,
    Refill_Supply INT,
    
    PRIMARY KEY(Refill_ID),
    FOREIGN KEY(PR_ID) REFERENCES PATIENT_PRESCRIPTIONS(PR_ID),
    FOREIGN KEY(Doc_ID) REFERENCES DOCTOR(Doc_ID)
    );

	

    
INSERT INTO HOSPITAL VALUES
	(987123, "MU HEALTH CARE", "1 Hospital Dr, Columbia, MO 65201");

INSERT INTO MEDICATIONS VALUES
	(1234, "Lisinopril"),
    (4321, "Duloxetine"),
    (9843, "Losartan"),
    (6529, "Zoloft");


INSERT INTO DOCTOR VALUES
	(10, "John", "Hopkins"),
    (11, "Tony", "Hawk"),
    (12, "Tom", " Holland");

INSERT INTO PATIENT VALUES
	(87923, "Carter", "Geruck", "1998-11-23", 5.7, 130.43, "1234 College Ave, Columbia, Missorui 65201",987123),
	(78125, "Chetan", "Vanteddu", "2003-12-25", 6.0, 168.12, "4000 E. Money Ave, Columbia, Missorui 65203",987123),
	(43129, "Alex", "Wiemon", "1978-10-11", 6.3, 190.35, "2300 Tiger Ave, Columbia, Missorui 65201", 987123);
    
INSERT INTO PHONE_NUMBERS VALUES
	(87923, 5431239876),
	(78125, 1239874598),
	(43129, 5418760978),
	(43129, 9827641232);
        
INSERT INTO PATIENT_PRESCRIPTIONS VALUES
	("A1234",87923, 6529),
    ("A1345",87923, 4321),
    ("A1236", 78125, 9843);
    

INSERT INTO REFILL_INFO (PR_ID, Refill_Date, Doc_ID, Dosage, Refill_Supply) VALUES
	("A1234", "2023-10-01", 10, 20, 30),
    ("A1234", "2023-11-01", 10, 20, 30),
    ("A1234", "2023-12-2", 10, 20, 30),
	("A1345", "2023-12-5", 10, 40, 30),
    ("A1236", "2023-09-22", 12, 40, 30),
    ("A1236", "2023-11-22", 12, 40, 30);

    
    

	
    
    





    


    
    
    
    
    
