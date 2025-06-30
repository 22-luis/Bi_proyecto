-- 1. Dimension: Date
CREATE TABLE dim_date (
    date_id INT IDENTITY(1,1) PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day INT,
    month INT,
    year INT,
    quarter INT,
    day_of_week INT
);

-- 2. Dimension: Vendor
CREATE TABLE dim_vendor (
    vendor_id VARCHAR(10) PRIMARY KEY,
    vendor_name VARCHAR(100),
    item_supplied VARCHAR(100),
    avg_lead_time_days INT,
    cost_per_item DECIMAL(12, 2),
    last_order_date DATE,
    next_delivery_date DATE
);

-- 3. Dimension: Staff
CREATE TABLE dim_staff (
    staff_id VARCHAR(10) PRIMARY KEY,
    staff_type VARCHAR(50)
);

-- 4. Dimension: Patient
CREATE TABLE dim_patient (
    patient_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100)
);

-- 5. Dimension: Medication
CREATE TABLE dim_medication (
    medication_id INT IDENTITY(1,1) PRIMARY KEY,
    medication_name VARCHAR(100) UNIQUE
);

-- 6. Dimension: Test Result
CREATE TABLE dim_patient_outcome (
    patient_outcome_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_outcome VARCHAR(50) UNIQUE
);
-- 7. Dimension: Admission Type
CREATE TABLE dim_admission_type (
    admission_type_id INT IDENTITY(1,1) PRIMARY KEY,
    admission_type VARCHAR(50) UNIQUE
);
-- 8. Dimension: Admission
CREATE TABLE dim_admission (
    admission_id INT IDENTITY(1,1) PRIMARY KEY,
	patient_id VARCHAR(10),
    admission_date DATETIME,
    discharge_date DATETIME,
    primary_diagnosis VARCHAR(100),
    procedure_performed VARCHAR(100),
    room_type VARCHAR(50),
    bed_days INT,
	medication_id INT,
	admission_type_id INT,
	patient_outcome_id INT,
	"registration_time" INT,
    "triage_time" INT,
    "medic_time" INT,
    "total_time" INT,
    "patient_satisfaction" INT,

	CONSTRAINT FK_admission_patient FOREIGN KEY (patient_id) REFERENCES dim_patient(patient_id) ON DELETE CASCADE,
	CONSTRAINT FK_admission_medication FOREIGN KEY (medication_id) REFERENCES dim_medication(medication_id) ON DELETE CASCADE,
    CONSTRAINT FK_admission_patient_outcome FOREIGN KEY (patient_outcome_id) REFERENCES dim_patient_outcome(patient_outcome_id) ON DELETE CASCADE,
	CONSTRAINT FK_admission_admission_type FOREIGN KEY (admission_type_id) REFERENCES dim_admission_type(admission_type_id) ON DELETE CASCADE
);



-- 9. Dimension: Item
CREATE TABLE dim_item (
    item_id INT PRIMARY KEY,
    item_type VARCHAR(50),
    item_name VARCHAR(100)
);

-- 10. Dimension: Resource
CREATE TABLE dim_resource (
    resource_id INT IDENTITY(1,1) PRIMARY KEY,
	resource_name VARCHAR(100),
    resource_category VARCHAR(100)
);

-- === Fact Tables ===

-- 11. Fact: Inventory
CREATE TABLE fact_inventory (
    inventory_id INT IDENTITY(1,1) PRIMARY KEY,
    date_id INT,
    item_id INT,
    current_stock INT,
    min_required INT,
    max_capacity INT,
    unit_cost DECIMAL(12, 2),
    avg_usage_per_day INT,
    restock_lead_time INT,
    vendor_id VARCHAR(10),

    CONSTRAINT FK_inventory_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE CASCADE,
    CONSTRAINT FK_inventory_item FOREIGN KEY (item_id) REFERENCES dim_item(item_id) ON DELETE CASCADE,
    CONSTRAINT FK_inventory_vendor FOREIGN KEY (vendor_id) REFERENCES dim_vendor(vendor_id) ON DELETE CASCADE
);

-- 12. Fact: Staff Shift
CREATE TABLE fact_staff_shift (
    shift_id INT IDENTITY(1,1) PRIMARY KEY,
    staff_id VARCHAR(10),
    shift_date DATE,
    shift_start_time TIME,
    shift_end_time TIME,
    current_assignment VARCHAR(100),
    hours_worked INT,
    patients_assigned INT,
    overtime_hours INT,

    CONSTRAINT FK_staff_shift_staff FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id) ON DELETE CASCADE
);

-- 13. Fact: Admission
CREATE TABLE fact_admission (
    fact_id INT IDENTITY(1,1) PRIMARY KEY,
    admission_id INT,
    supplies_used VARCHAR(255),
    equipment_used VARCHAR(100),
    nurse_ratio VARCHAR(100),
    total_cost INT,

    CONSTRAINT FK_fact_admission FOREIGN KEY (admission_id) REFERENCES dim_admission(admission_id) ON DELETE CASCADE
);

-- 15. Fact: Expenses
CREATE TABLE fact_expense (
    expense_id INT IDENTITY(1,1) PRIMARY KEY,
    admission_id INT,
    resource_id INT,
    cost DECIMAL(14, 2)

    CONSTRAINT FK_expense_admission FOREIGN KEY (admission_id) REFERENCES dim_admission(admission_id) ON DELETE CASCADE,
    CONSTRAINT FK_expense_resource FOREIGN KEY (resource_id) REFERENCES dim_resource(resource_id) ON DELETE CASCADE
);
