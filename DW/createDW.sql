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

-- 4. Dimension: Patient (basic)
CREATE TABLE dim_patient (
    patient_id VARCHAR(10) PRIMARY KEY
);

-- 5. Dimension: Patient Detail (extending patient)
CREATE TABLE dim_patient_detail (
    patient_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100)
);

-- 6. Dimension: Admission Type
CREATE TABLE dim_admission_type (
    admission_type_id INT IDENTITY(1,1) PRIMARY KEY,
    admission_type VARCHAR(50) UNIQUE
);

-- 7. Dimension: Medication
CREATE TABLE dim_medication (
    medication_id INT IDENTITY(1,1) PRIMARY KEY,
    medication_name VARCHAR(100) UNIQUE
);

-- 8. Dimension: Test Result
CREATE TABLE dim_test_result (
    test_result_id INT IDENTITY(1,1) PRIMARY KEY,
    test_result VARCHAR(50) UNIQUE
);

-- 9. Dimension: Item
CREATE TABLE dim_item (
    item_id INT PRIMARY KEY,
    item_type VARCHAR(50),
    item_name VARCHAR(100)
);

-- 10. Dimension: Expense Category
CREATE TABLE dim_expense_category (
    expense_category_id INT IDENTITY(1,1) PRIMARY KEY,
    expense_category VARCHAR(100) UNIQUE
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

    CONSTRAINT FK_inventory_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    CONSTRAINT FK_inventory_item FOREIGN KEY (item_id) REFERENCES dim_item(item_id),
    CONSTRAINT FK_inventory_vendor FOREIGN KEY (vendor_id) REFERENCES dim_vendor(vendor_id)
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

    CONSTRAINT FK_staff_shift_staff FOREIGN KEY (staff_id) REFERENCES dim_staff(staff_id)
);

-- 13. Fact: Patient Stay
CREATE TABLE fact_patient_stay (
    stay_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id VARCHAR(10),
    admission_date DATETIME,
    discharge_date DATETIME,
    primary_diagnosis VARCHAR(100),
    procedure_performed VARCHAR(100),
    room_type VARCHAR(50),
    bed_days INT,
    supplies_used VARCHAR(255),
    equipment_used VARCHAR(100),
    staff_needed VARCHAR(100),
    total_cost INT,

    CONSTRAINT FK_patient_stay_patient FOREIGN KEY (patient_id) REFERENCES dim_patient(patient_id)
);

-- 14. Fact: Patient Health Details
CREATE TABLE fact_patient_health (
    fact_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id VARCHAR(10),
    admission_type_id INT,
    medication_id INT,
    test_result_id INT,

    CONSTRAINT FK_patient_health_patient FOREIGN KEY (patient_id) REFERENCES dim_patient_detail(patient_id),
    CONSTRAINT FK_patient_health_admission FOREIGN KEY (admission_type_id) REFERENCES dim_admission_type(admission_type_id),
    CONSTRAINT FK_patient_health_medication FOREIGN KEY (medication_id) REFERENCES dim_medication(medication_id),
    CONSTRAINT FK_patient_health_test_result FOREIGN KEY (test_result_id) REFERENCES dim_test_result(test_result_id)
);

-- 15. Fact: Expenses
CREATE TABLE fact_expense (
    expense_id INT IDENTITY(1,1) PRIMARY KEY,
    date_id INT,
    expense_category_id INT,
    amount DECIMAL(14, 2),
    description VARCHAR(255),

    CONSTRAINT FK_expense_date FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    CONSTRAINT FK_expense_category FOREIGN KEY (expense_category_id) REFERENCES dim_expense_category(expense_category_id)
);
