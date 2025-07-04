**Diccionario de Datos: patient_data**

| Nombre del Dato     | Descripción                                                |
|---------------------|------------------------------------------------------------|
| Patient_ID          | Identificador único del paciente                           |
| Name                | Nombre completo del paciente                               |
| Age                 | Edad del paciente en años                                  |
| Gender              | Género del paciente (por ejemplo, Male o Female)           |
| Blood Type          | Tipo de sangre del paciente (por ejemplo, A+, O-, etc.)    |
| Medical Condition   | Condición médica principal diagnosticada                   |

**Diccionario de Datos: vendor_data**

| Nombre del Dato         | Descripción                                                    |
|-------------------------|----------------------------------------------------------------|
| Vendor_ID               | Identificador único del proveedor                              |
| Vendor_Name             | Nombre de la empresa o proveedor                               |
| Item_Supplied           | Nombre del artículo suministrado por el proveedor              |
| Avg_Lead_Time (days)    | Tiempo promedio en días que tarda en entregar el artículo      |
| Cost_Per_Item           | Costo por unidad del artículo suministrado                     |
| Last_Order_Date         | Fecha del último pedido realizado al proveedor                 |
| Next_Delivery_Date      | Fecha estimada para la próxima entrega                         |

**Diccionario de Datos: admission_data**

| Nombre del Dato        | Descripción                                                        |
|------------------------|--------------------------------------------------------------------|
| Patient_ID             | Identificador único del paciente                                   |
| Admission_Date         | Fecha y hora de ingreso del paciente                               |
| Discharge_Date         | Fecha y hora de alta del paciente                                  |
| Primary_Diagnosis      | Diagnóstico principal al momento del ingreso                       |
| Admission_Type         | Tipo de admisión al hospital (por ejemplo, Critical)               |
| Procedure_Performed    | Procedimiento médico realizado durante la estancia                 |
| Room_Type              | Tipo de habitación asignada al paciente                            |
| Bed_Days               | Número de días que el paciente ocupó una cama                      |
| Supplies_Used          | Insumos médicos utilizados durante la estancia (ej. guantes, IV)   |
| Equipment_Used         | Equipos médicos utilizados (ej. mesa quirúrgica)                   |
| Nurse_Ratio            | Proporcion de enfermeros atendiendo al paciente                    |
| Medication             | Medicamento administrado al paciente                               |
| Patient_Outcome        | Resultado del encuentro principal con el paciente (ej. Admitted)   |
| Time to Registration   | Tiempo desde que el paciente llega hasta que se registra (min)     |
| Time_to_Triage         | Tiempo desde que el paciente se registra hasta que llega a triaje  |
| Time_to_Medic          | Tiempo desde triaje hasta que el paciente ve a un medico (min)     |
| Total_Wait_Time        | Tiempo total de espera (min)                                       |
| Patient_Satisfaction   | Nivel de satisfaccion del paciente con su servicio del 1 al 5      |

**Diccionario de Datos: expense_data**

| Nombre del Dato     | Descripción                                                    |
|---------------------|----------------------------------------------------------------|
| Admission ID        | Identificador unico de la admision a la que pertence el gasto  |
| Expense ID          | Identificador unico del gasto                                  |
| Resource Name       | Nombre del recurso utilizado                                   |
| Resource Type       | Categoría a la que pertenece el gasto (ej. Personal, Suministros) |
| Resource Cost       | Monto total del gasto registrado                               |

**Diccionario de Datos: staff_shift_data**

| Nombre del Dato       | Descripción                                                        |
|-----------------------|--------------------------------------------------------------------|
| Staff_ID              | Identificador único del miembro del personal                       |
| Staff_Type            | Tipo de personal (por ejemplo, Surgeon, Nurse, Technician)        |
| Shift_Date            | Fecha del turno                                                     |
| Shift_Start_Time      | Hora de inicio del turno                                           |
| Shift_End_Time        | Hora de finalización del turno                                     |
| Current_Assignment    | Área o unidad en la que está asignado durante el turno             |
| Hours_Worked          | Total de horas trabajadas en el turno                              |
| Patients_Assigned     | Número de pacientes asignados durante el turno                     |
| Overtime_Hours        | Horas extras trabajadas fuera del horario regular                  |

**Diccionario de Datos: inventory_data**

| Nombre del Dato        | Descripción                                                        |
|------------------------|--------------------------------------------------------------------|
| Date                   | Fecha del registro de inventario                                   |
| Item_ID                | Identificador único del artículo                                   |
| Item_Type              | Tipo de artículo (por ejemplo, Consumable, Equipment)             |
| Item_Name              | Nombre del artículo                                                |
| Current_Stock          | Cantidad actual en inventario                                     |
| Min_Required           | Cantidad mínima requerida para mantener en inventario             |
| Max_Capacity           | Capacidad máxima de almacenamiento del artículo                   |
| Unit_Cost              | Costo por unidad del artículo                                      |
| Avg_Usage_Per_Day      | Uso promedio diario del artículo                                  |
| Restock_Lead_Time      | Tiempo promedio en días para reabastecer el artículo              |
| Vendor_ID              | Identificador del proveedor que suministra el artículo            |
