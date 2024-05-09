from datetime import datetime, timedelta
import pandas as pd
import warnings
from colorama import Fore, Back, Style

#Helper function that calculates a patients PDC ratio which will help predict a patients adherance to a medication
def pdc_r(fill_dates, days_supply, start_date, end_date):
    
    warnings.simplefilter('ignore')
    #return of 0 alerts patient's care team that patient is already not 
    # adhering to their perscription after one refill; 1 means that there has only been 1 refill in patient's refill history and are for adhering to their perscription
    #if len(fill_dates) == 1:
        #if abs((fill_dates[0] - datetime.now()).days) > days_supply[0]:
            #pdc_ratio = 0
            #return pdc_ratio
        #else:
           # pdc_ratio = 1
            #return pdc_ratio
        
    if len(fill_dates) != len(days_supply):
        raise ValueError("inputs must be of same length")
        
    
    supply_deltas = pd.Series([pd.to_timedelta(days, unit='D') for days in days_supply], index=fill_dates)

    
    supply_enddates = supply_deltas + supply_deltas.index

    supply_enddates[supply_enddates > end_date] = end_date


    new_deltas  = supply_enddates - supply_enddates.index

    covered_days  = new_deltas.sum()
    total_days =  end_date - supply_deltas.index.min()
    pdc_ratio = covered_days/total_days

    return pdc_ratio

# THis function creates a new prescription for an existing patient

def create_prescription(cursor, db):
    print()
    Patient_ID = input("Please enter the Patient ID of the patient you would like to add a prescription to (or type q to go back): ")
    if Patient_ID == 'q':
        return
    print()
    PR_ID = input("Please assign a Prescription Identifier for  " + Patient_ID + "'s new prescription: ")
    print()
    Med_ID = input("Please enter the medication id: ")
    print()
    Doc_ID = input("Please enter the prescribing doctor's ID: ")
    print()
    Dosage = input("Please enter the prescribed dosage for this prescription: ")
    print()
    Refill_Supply = input("Please enter the refill quantity: ")
    print()
    print()

    query = "INSERT INTO PATIENT_PRESCRIPTIONS VALUES (%s, %s, %s)"
    cursor.execute(query, (PR_ID, Patient_ID, Med_ID))
    db.commit()


    form_date = datetime.now()
    query = "INSERT INTO REFILL_INFO (PR_ID, Refill_Date, Doc_ID, Dosage, Refill_Supply) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (PR_ID, form_date, Doc_ID, Dosage, Refill_Supply))
    db.commit()

    cursor.execute("SELECT * FROM PATIENT_PRESCRIPTIONS")
   
    print(Fore.WHITE + Back.GREEN + "Prescription has been added to " + Patient_ID + "'s record!" + Style.RESET_ALL)         
    print()
    
    input("Press ENTER to return to menu")   

# Ths function allows a care team to delete an existing patient's prescription

def delete_prescription(cursor, db):
    print()
    PR_ID = input("Please enter the Prescription Identifier of the prescription you would like to delete: ")
    print()

    query = "DELETE FROM REFILL_INFO WHERE PR_ID = %s" 
    cursor.execute(query, (PR_ID,))
    db.commit()

    query = "DELETE FROM PATIENT_PRESCRIPTIONS WHERE PR_ID = %s" 
    cursor.execute(query, (PR_ID,))
    db.commit()


    print(Fore.WHITE + Back.GREEN + "Prescription " + PR_ID + " has been deleted!" + Style.RESET_ALL)
    print()
    input("Press ENTER to return to menu")
    
# This function gets a patient's PDC ratio and then determines if a patient has been adhering to their medication

def check_adherence(cursor):
    PR_ID = input("Please enter patient' Prescription ID: ")
    print()

    query = "SELECT Refill_Date, Refill_Supply FROM REFILL_INFO WHERE PR_ID = %s ORDER BY Refill_Date ASC"
    cursor.execute(query, (PR_ID,))

    result = cursor.fetchall()

    fill_dates, days_supply = map(list, zip(*result))


    maxy = len(fill_dates)
    start_date = fill_dates[0]
    end_date = fill_dates[maxy-1]

    pdc_ratio = (pdc_r(fill_dates,days_supply, start_date, end_date))*100
    if pdc_ratio == 0:
        print("This patient has completed their first refill of their medication, but have not yet got a refill")
    elif pdc_ratio == 1:
        print("Patient has started taking their perscription and still has time before they need to refill their prescription")
    elif pdc_ratio >= 80.0:
        print(Fore.BLACK + Back.GREEN + "This patient has been adhering to their medication and has a Proportion of Days Covered score of  " + str(pdc_ratio) + Style.RESET_ALL)
    else:
        print(Fore.BLACK + Back.RED + "Patient has not been taking their prescribed medication regularly and has a Proportion of Days Covered score of " + str(pdc_ratio) + Style.RESET_ALL)

    print()
    input("Press ENTER to return to menu")


def view_prescriptions(cursor):
    cursor.execute("""
        SELECT PATIENT.Fname, PATIENT.Lname, MEDICATIONS.Med_Name, PATIENT_PRESCRIPTIONS.Med_ID
        FROM PATIENT_PRESCRIPTIONS
        INNER JOIN PATIENT ON PATIENT_PRESCRIPTIONS.Patient_ID = PATIENT.Patient_ID
        INNER JOIN MEDICATIONS ON PATIENT_PRESCRIPTIONS.Med_ID = MEDICATIONS.Med_ID
    """)
    print("View of Patient's Prescriptions:")
    print()
    for x in cursor:
        print(f"{x[1]},{x[0]} has the following prescriptions: {x[2]} (# {x[3]})")
    print()

    cursor.execute("""
    SELECT PATIENT.Fname, PATIENT.Lname, MEDICATIONS.Med_Name, MEDICATIONS.Med_ID, REFILL_INFO.Refill_Date, REFILL_INFO.Dosage
    FROM PATIENT_PRESCRIPTIONS
    INNER JOIN PATIENT ON PATIENT_PRESCRIPTIONS.Patient_ID = PATIENT.Patient_ID
    INNER JOIN MEDICATIONS ON PATIENT_PRESCRIPTIONS.Med_ID = MEDICATIONS.Med_ID
    INNER JOIN REFILL_INFO ON PATIENT_PRESCRIPTIONS.PR_ID = REFILL_INFO.PR_ID
    """)
    print("View of REFILL_INFO Table")
    print()
    for y in cursor:
        print(f"{y[1]},{y[0]} has refill medication {y[2]} (# {y[3]}) on {y[4]}")
    print()








    

