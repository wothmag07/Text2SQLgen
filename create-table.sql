
CREATE TABLE llm.heartattack_data (
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
);

CREATE TABLE llm.breastcancer_data (
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
);

CREATE TABLE llm.livercirrhosis_data (
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
);
CREATE TABLE llm.diabetes_data (
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
);

CREATE TABLE llm.glaucoma_Data (
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
);