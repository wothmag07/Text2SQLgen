import psycopg2
from db_config import read_db_config
import logging

logging.basicConfig(level=logging.DEBUG)


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Read connection parameters
        params = read_db_config()

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor
        cur = conn.cursor()

        # Execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # Display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # Create tables and copy data
        create_tables_and_copy_data(conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_tables_and_copy_data(conn):
    """ Create tables and copy data """
    try:
        # Execute SQL statements to create tables
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE llm.heartattack_data (
                            PatientID INT PRIMARY KEY,
                            Age INT,
                            Sex TEXT,
                            Cholesterol TEXT,
                            BloodPressure TEXT,
                            HeartRate INT,
                            Diabetes INT,
                            FamilyHistory INT,
                            Smoking INT,
                            Obesity INT,
                            AlcoholConsumption FLOAT,
                            ExerciseHoursPerWeek FLOAT,
                            Diet TEXT,
                            PreviousHeartProblems INT,
                            MedicationUse INT,
                            StressLevel FLOAT,
                            SedentaryHoursPerDay FLOAT,
                            Income INT,
                            BMI FLOAT,
                            Triglycerides INT,
                            PhysicalActivityDaysPerWeek INT,
                            SleepHoursPerDay FLOAT,
                            Country TEXT,
                            Continent TEXT,
                            Hemisphere TEXT,
                            HeartAttackRisk INT
                            );''')
            cur.execute('''CREATE TABLE llm.breastcancer_data (
                            Patient_Id INT PRIMARY KEY,
                            Class TEXT,
                            Age TEXT,
                            Menopause TEXT,
                            Tumor_size TEXT,
                            Inv_nodes TEXT,
                            Node_caps TEXT,
                            Deg_malig INT,
                            Breast TEXT,
                            Breast_quad TEXT,
                            Irradiat TEXT
                            );''')
            cur.execute('''CREATE TABLE llm.livercirrhosis_data (
                            Patient_Id INT PRIMARY KEY,
                            Age INT,
                            Albumin FLOAT,
                            Alk_Phos FLOAT,
                            Ascites TEXT,
                            Bilirubin FLOAT,
                            Cholesterol INT,
                            Copper INT,
                            Drug TEXT,
                            Edema TEXT,
                            Hepatomegaly TEXT,
                            N_Days INT,
                            Platelets INT,
                            Prothrombin FLOAT,
                            SGOT FLOAT,
                            Sex TEXT,
                            Spiders TEXT,
                            Stage INT,
                            Status TEXT,
                            Tryglicerides INT
                        );''')
            cur.execute('''CREATE TABLE llm.diabetes_data (
                            Patient_Id INT PRIMARY KEY,
                            Age INT,
                            BMI DECIMAL,
                            BloodPressure INT,
                            DiabetesPedigreeFunction DECIMAL,
                            Glucose INT,
                            Insulin INT,
                            Outcome INT,
                            Pregnancies INT,
                            SkinThickness INT
                        );''')
            cur.execute('''CREATE TABLE llm.glaucoma_Data (
                            Patient_ID INT PRIMARY KEY,
                            Age INT,
                            Angle_Closure_Status TEXT,
                            Cataract_Status TEXT,
                            Cup_to_Disc_Ratio FLOAT,
                            Diagnosis TEXT,
                            Family_History TEXT,
                            Gender TEXT,
                            Glaucoma_Type TEXT,
                            Intraocular_Pressure FLOAT,
                            Medical_History TEXT,
                            Medication_Usage TEXT,
                            Optical_Coherence_Tomography_Results TEXT,
                            Pachymetry FLOAT,
                            Visual_Acuity_Measurements TEXT,
                            Visual_Field_Test_Results TEXT,
                            Visual_Symptoms TEXT
                        );''')

        # Execute SQL statements to copy data
        with conn.cursor() as cur:
            cur.execute('''COPY llm.heartattack_data FROM 'D:\\Workspace\\LLM\\Text2SQLgen\\datatables\\heart_attack_prediction_dataset.csv' WITH CSV HEADER;''')
            cur.execute('''COPY llm.breastcancer_data FROM 'D:\\Workspace\\LLM\\Text2SQLgen\\datatables\\breast-cancer.csv' WITH CSV HEADER;''')
            cur.execute('''COPY llm.diabetes_data FROM 'D:\\Workspace\\LLM\\Text2SQLgen\\datatables\\diabetes.csv' WITH CSV HEADER;''')
            cur.execute('''COPY llm.glaucoma_Data FROM 'D:\\Workspace\\LLM\\Text2SQLgen\\datatables\\glaucoma_dataset.csv' WITH CSV HEADER;''')
            cur.execute('''COPY llm.livercirrhosis_data FROM 'D:\\Workspace\\LLM\\Text2SQLgen\\datatables\\cirrhosis.csv' WITH CSV HEADER;''')

        # Commit the changes
        conn.commit()

        print('Tables created and data copied successfully.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    connect()
