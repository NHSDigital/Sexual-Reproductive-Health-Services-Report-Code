SELECT [PatientID]
    ,[RowNum]
    ,[OrgID] as Org_code
    ,[OrgName] as Org_name
    ,[ClinicID] as Clinic_code
    ,[ClinicName] as Clinic_name
    ,[ClinicLA] as Clinic_LA_code_lower
    ,[ClinicLAName] as Clinic_LA_name_lower
    ,[ClinicUpperLACode] as Clinic_LA_code_upper
    ,[ClinicUpperLAName] as Clinic_LA_name_upper
    ,[Gender]    
    ,[Age]
    ,[Ethnicity]
    ,[UpperLACode] as LA_code
    ,[UpperLAName] as LA_name
    ,[LAofResidence] as LA_code_lower
    ,[LAName] as LA_name_lower
    ,[LAParent] as LA_parent_code
    ,[LSOA] as LSOA_code
    ,[GeneralMedicalPractice] as GP_code
    ,[DateofAttendance]
    ,[InitialContact]
    ,[MainContact]
    ,[FirstContact]
    ,[LocationType] 
    ,[ConsultationMedium]   
    ,[ContraceptiveMethodStatus]
    ,[ContraceptiveMainMethod]
    ,[ContraceptiveOtherMethod1]
    ,[ContraceptiveOtherMethod2]
    ,[EmergencyContraceptionFlag]
    ,[ContraceptiveMethodPostCoital1]
    ,[ContraceptiveMethodPostCoital2]
    ,[SRHCareActivity1]
    ,[SRHCareActivity2]
    ,[SRHCareActivity3]
    ,[SRHCareActivity4]
    ,[SRHCareActivity5]
    ,[SRHCareActivity6]
    ,[SRHCareActivityFLag]
    ,[ReportingYear]
FROM [<Database>].[schema].[<Table>]