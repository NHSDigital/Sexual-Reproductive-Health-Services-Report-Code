/*
Creates a count of vasectomy and sterlisation procedures by age and patient type
from the APC and Outpatients databases.
Vasectomy data is split into Inpatients/Daycases/Outpatients
Vasectomy reversals, sterilisations and sterilisation reversals are split into
All APC/Outpatients

*/


/*
Select inpatient vasectomies
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [STARTAGE] as Age,
    'Inpatients' as PatientType,
    'Vasectomies' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableAPC>]
WHERE SEX = 1
AND [CLASSPAT] IN ('1', '5')
AND [EPISTAT] = '3'
AND (
    OPERTN_4_01 IN ('<ProcListVas>')
    OR OPERTN_4_02 IN ('<ProcListVas>')
    OR OPERTN_4_03 IN ('<ProcListVas>')
    OR OPERTN_4_04 IN ('<ProcListVas>')
    OR OPERTN_4_05 IN ('<ProcListVas>')
    OR OPERTN_4_06 IN ('<ProcListVas>')
    OR OPERTN_4_07 IN ('<ProcListVas>')
    OR OPERTN_4_08 IN ('<ProcListVas>')
    OR OPERTN_4_09 IN ('<ProcListVas>')
    OR OPERTN_4_10 IN ('<ProcListVas>')
    OR OPERTN_4_11 IN ('<ProcListVas>')
    OR OPERTN_4_12 IN ('<ProcListVas>')
    OR OPERTN_4_13 IN ('<ProcListVas>')
    OR OPERTN_4_14 IN ('<ProcListVas>')
    OR OPERTN_4_15 IN ('<ProcListVas>')
    OR OPERTN_4_16 IN ('<ProcListVas>')
    OR OPERTN_4_17 IN ('<ProcListVas>')
    OR OPERTN_4_18 IN ('<ProcListVas>')
    OR OPERTN_4_19 IN ('<ProcListVas>')
    OR OPERTN_4_20 IN ('<ProcListVas>')
    OR OPERTN_4_21 IN ('<ProcListVas>')
    OR OPERTN_4_22 IN ('<ProcListVas>')
    OR OPERTN_4_23 IN ('<ProcListVas>')
    OR OPERTN_4_24 IN ('<ProcListVas>'))

GROUP BY [FYEAR], [STARTAGE]

UNION ALL

/*
Select day case vasectomies
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [STARTAGE] as Age,
    'Day cases' as PatientType,
    'Vasectomies' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableAPC>]
WHERE SEX = 1
AND [CLASSPAT] = '2'
AND [EPISTAT] = '3'
AND (
    OPERTN_4_01 IN ('<ProcListVas>')
    OR OPERTN_4_02 IN ('<ProcListVas>')
    OR OPERTN_4_03 IN ('<ProcListVas>')
    OR OPERTN_4_04 IN ('<ProcListVas>')
    OR OPERTN_4_05 IN ('<ProcListVas>')
    OR OPERTN_4_06 IN ('<ProcListVas>')
    OR OPERTN_4_07 IN ('<ProcListVas>')
    OR OPERTN_4_08 IN ('<ProcListVas>')
    OR OPERTN_4_09 IN ('<ProcListVas>')
    OR OPERTN_4_10 IN ('<ProcListVas>')
    OR OPERTN_4_11 IN ('<ProcListVas>')
    OR OPERTN_4_12 IN ('<ProcListVas>')
    OR OPERTN_4_13 IN ('<ProcListVas>')
    OR OPERTN_4_14 IN ('<ProcListVas>')
    OR OPERTN_4_15 IN ('<ProcListVas>')
    OR OPERTN_4_16 IN ('<ProcListVas>')
    OR OPERTN_4_17 IN ('<ProcListVas>')
    OR OPERTN_4_18 IN ('<ProcListVas>')
    OR OPERTN_4_19 IN ('<ProcListVas>')
    OR OPERTN_4_20 IN ('<ProcListVas>')
    OR OPERTN_4_21 IN ('<ProcListVas>')
    OR OPERTN_4_22 IN ('<ProcListVas>')
    OR OPERTN_4_23 IN ('<ProcListVas>')
    OR OPERTN_4_24 IN ('<ProcListVas>'))

GROUP BY [FYEAR], [STARTAGE]

UNION ALL

/*
Select outpatient vasectomies
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [APPTAGE] as Age,
    'Outpatients' as PatientType,
    'Vasectomies' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableOP>]
WHERE SEX = 1
AND (
    OPERTN_4_01 IN ('<ProcListVas>')
    OR OPERTN_4_02 IN ('<ProcListVas>')
    OR OPERTN_4_03 IN ('<ProcListVas>')
    OR OPERTN_4_04 IN ('<ProcListVas>')
    OR OPERTN_4_05 IN ('<ProcListVas>')
    OR OPERTN_4_06 IN ('<ProcListVas>')
    OR OPERTN_4_07 IN ('<ProcListVas>')
    OR OPERTN_4_08 IN ('<ProcListVas>')
    OR OPERTN_4_09 IN ('<ProcListVas>')
    OR OPERTN_4_10 IN ('<ProcListVas>')
    OR OPERTN_4_11 IN ('<ProcListVas>')
    OR OPERTN_4_12 IN ('<ProcListVas>')
    OR OPERTN_4_13 IN ('<ProcListVas>')
    OR OPERTN_4_14 IN ('<ProcListVas>')
    OR OPERTN_4_15 IN ('<ProcListVas>')
    OR OPERTN_4_16 IN ('<ProcListVas>')
    OR OPERTN_4_17 IN ('<ProcListVas>')
    OR OPERTN_4_18 IN ('<ProcListVas>')
    OR OPERTN_4_19 IN ('<ProcListVas>')
    OR OPERTN_4_20 IN ('<ProcListVas>')
    OR OPERTN_4_21 IN ('<ProcListVas>')
    OR OPERTN_4_22 IN ('<ProcListVas>')
    OR OPERTN_4_23 IN ('<ProcListVas>')
    OR OPERTN_4_24 IN ('<ProcListVas>'))

GROUP BY [FYEAR], [APPTAGE]

UNION ALL

/*
Select inpatient and day case vasectomy reversals
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [STARTAGE] as Age,
    'All APC' as PatientType,
    'Vasectomy_reversals' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableAPC>]
WHERE SEX = 1
AND [CLASSPAT] IN ('1', '2', '5')
AND [EPISTAT] = '3'
AND (
    OPERTN_4_01 IN ('<ProcListVasRev>')
    OR OPERTN_4_02 IN ('<ProcListVasRev>')
    OR OPERTN_4_03 IN ('<ProcListVasRev>')
    OR OPERTN_4_04 IN ('<ProcListVasRev>')
    OR OPERTN_4_05 IN ('<ProcListVasRev>')
    OR OPERTN_4_06 IN ('<ProcListVasRev>')
    OR OPERTN_4_07 IN ('<ProcListVasRev>')
    OR OPERTN_4_08 IN ('<ProcListVasRev>')
    OR OPERTN_4_09 IN ('<ProcListVasRev>')
    OR OPERTN_4_10 IN ('<ProcListVasRev>')
    OR OPERTN_4_11 IN ('<ProcListVasRev>')
    OR OPERTN_4_12 IN ('<ProcListVasRev>')
    OR OPERTN_4_13 IN ('<ProcListVasRev>')
    OR OPERTN_4_14 IN ('<ProcListVasRev>')
    OR OPERTN_4_15 IN ('<ProcListVasRev>')
    OR OPERTN_4_16 IN ('<ProcListVasRev>')
    OR OPERTN_4_17 IN ('<ProcListVasRev>')
    OR OPERTN_4_18 IN ('<ProcListVasRev>')
    OR OPERTN_4_19 IN ('<ProcListVasRev>')
    OR OPERTN_4_20 IN ('<ProcListVasRev>')
    OR OPERTN_4_21 IN ('<ProcListVasRev>')
    OR OPERTN_4_22 IN ('<ProcListVasRev>')
    OR OPERTN_4_23 IN ('<ProcListVasRev>')
    OR OPERTN_4_24 IN ('<ProcListVasRev>'))

GROUP BY [FYEAR], [STARTAGE]


UNION ALL

/*
Select inpatient and day case sterlisations
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [STARTAGE] as Age,
    'All APC' as PatientType,
    'Sterilisations' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableAPC>]
WHERE SEX = 2
AND [CLASSPAT] IN ('1', '2', '5')
AND [EPISTAT] = '3'
AND (
    OPERTN_4_01 IN ('<ProcListSter>')
    OR OPERTN_4_02 IN ('<ProcListSter>')
    OR OPERTN_4_03 IN ('<ProcListSter>')
    OR OPERTN_4_04 IN ('<ProcListSter>')
    OR OPERTN_4_05 IN ('<ProcListSter>')
    OR OPERTN_4_06 IN ('<ProcListSter>')
    OR OPERTN_4_07 IN ('<ProcListSter>')
    OR OPERTN_4_08 IN ('<ProcListSter>')
    OR OPERTN_4_09 IN ('<ProcListSter>')
    OR OPERTN_4_10 IN ('<ProcListSter>')
    OR OPERTN_4_11 IN ('<ProcListSter>')
    OR OPERTN_4_12 IN ('<ProcListSter>')
    OR OPERTN_4_13 IN ('<ProcListSter>')
    OR OPERTN_4_14 IN ('<ProcListSter>')
    OR OPERTN_4_15 IN ('<ProcListSter>')
    OR OPERTN_4_16 IN ('<ProcListSter>')
    OR OPERTN_4_17 IN ('<ProcListSter>')
    OR OPERTN_4_18 IN ('<ProcListSter>')
    OR OPERTN_4_19 IN ('<ProcListSter>')
    OR OPERTN_4_20 IN ('<ProcListSter>')
    OR OPERTN_4_21 IN ('<ProcListSter>')
    OR OPERTN_4_22 IN ('<ProcListSter>')
    OR OPERTN_4_23 IN ('<ProcListSter>')
    OR OPERTN_4_24 IN ('<ProcListSter>'))

GROUP BY [FYEAR], [STARTAGE]

UNION ALL

/*
Select outpatient sterlisations
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [APPTAGE] as Age,
    'Outpatients' as PatientType,
    'Sterilisations' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableOP>]
WHERE SEX = 2
AND (
    OPERTN_4_01 IN ('<ProcListSter>')
    OR OPERTN_4_02 IN ('<ProcListSter>')
    OR OPERTN_4_03 IN ('<ProcListSter>')
    OR OPERTN_4_04 IN ('<ProcListSter>')
    OR OPERTN_4_05 IN ('<ProcListSter>')
    OR OPERTN_4_06 IN ('<ProcListSter>')
    OR OPERTN_4_07 IN ('<ProcListSter>')
    OR OPERTN_4_08 IN ('<ProcListSter>')
    OR OPERTN_4_09 IN ('<ProcListSter>')
    OR OPERTN_4_10 IN ('<ProcListSter>')
    OR OPERTN_4_11 IN ('<ProcListSter>')
    OR OPERTN_4_12 IN ('<ProcListSter>')
    OR OPERTN_4_13 IN ('<ProcListSter>')
    OR OPERTN_4_14 IN ('<ProcListSter>')
    OR OPERTN_4_15 IN ('<ProcListSter>')
    OR OPERTN_4_16 IN ('<ProcListSter>')
    OR OPERTN_4_17 IN ('<ProcListSter>')
    OR OPERTN_4_18 IN ('<ProcListSter>')
    OR OPERTN_4_19 IN ('<ProcListSter>')
    OR OPERTN_4_20 IN ('<ProcListSter>')
    OR OPERTN_4_21 IN ('<ProcListSter>')
    OR OPERTN_4_22 IN ('<ProcListSter>')
    OR OPERTN_4_23 IN ('<ProcListSter>')
    OR OPERTN_4_24 IN ('<ProcListSter>'))

GROUP BY [FYEAR], [APPTAGE]

UNION ALL

/*
Select inpatient and day case sterlisation reversals
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [STARTAGE] as Age,
    'All APC' as PatientType,
    'Sterilisation reversals' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableAPC>]
WHERE SEX = 2
AND [CLASSPAT] IN ('1', '2')
AND [EPISTAT] = '3'
AND (
    OPERTN_4_01 IN ('<ProcListSterRev>')
    OR OPERTN_4_02 IN ('<ProcListSterRev>')
    OR OPERTN_4_03 IN ('<ProcListSterRev>')
    OR OPERTN_4_04 IN ('<ProcListSterRev>')
    OR OPERTN_4_05 IN ('<ProcListSterRev>')
    OR OPERTN_4_06 IN ('<ProcListSterRev>')
    OR OPERTN_4_07 IN ('<ProcListSterRev>')
    OR OPERTN_4_08 IN ('<ProcListSterRev>')
    OR OPERTN_4_09 IN ('<ProcListSterRev>')
    OR OPERTN_4_10 IN ('<ProcListSterRev>')
    OR OPERTN_4_11 IN ('<ProcListSterRev>')
    OR OPERTN_4_12 IN ('<ProcListSterRev>')
    OR OPERTN_4_13 IN ('<ProcListSterRev>')
    OR OPERTN_4_14 IN ('<ProcListSterRev>')
    OR OPERTN_4_15 IN ('<ProcListSterRev>')
    OR OPERTN_4_16 IN ('<ProcListSterRev>')
    OR OPERTN_4_17 IN ('<ProcListSterRev>')
    OR OPERTN_4_18 IN ('<ProcListSterRev>')
    OR OPERTN_4_19 IN ('<ProcListSterRev>')
    OR OPERTN_4_20 IN ('<ProcListSterRev>')
    OR OPERTN_4_21 IN ('<ProcListSterRev>')
    OR OPERTN_4_22 IN ('<ProcListSterRev>')
    OR OPERTN_4_23 IN ('<ProcListSterRev>')
    OR OPERTN_4_24 IN ('<ProcListSterRev>'))

GROUP BY [FYEAR], [STARTAGE]

UNION ALL

/*
Select outpatient sterlisation reversals
*/
SELECT DISTINCT
    [FYEAR] as ReportingYear,
    [APPTAGE] as Age,
    'Outpatients' as PatientType,
    'Sterilisation reversals' as ProcType,
    count(*) as 'Count'
FROM [<Database>].[schema].[<TableOP>]
WHERE SEX = 2
AND (
    OPERTN_4_01 IN ('<ProcListSterRev>')
    OR OPERTN_4_02 IN ('<ProcListSterRev>')
    OR OPERTN_4_03 IN ('<ProcListSterRev>')
    OR OPERTN_4_04 IN ('<ProcListSterRev>')
    OR OPERTN_4_05 IN ('<ProcListSterRev>')
    OR OPERTN_4_06 IN ('<ProcListSterRev>')
    OR OPERTN_4_07 IN ('<ProcListSterRev>')
    OR OPERTN_4_08 IN ('<ProcListSterRev>')
    OR OPERTN_4_09 IN ('<ProcListSterRev>')
    OR OPERTN_4_10 IN ('<ProcListSterRev>')
    OR OPERTN_4_11 IN ('<ProcListSterRev>')
    OR OPERTN_4_12 IN ('<ProcListSterRev>')
    OR OPERTN_4_13 IN ('<ProcListSterRev>')
    OR OPERTN_4_14 IN ('<ProcListSterRev>')
    OR OPERTN_4_15 IN ('<ProcListSterRev>')
    OR OPERTN_4_16 IN ('<ProcListSterRev>')
    OR OPERTN_4_17 IN ('<ProcListSterRev>')
    OR OPERTN_4_18 IN ('<ProcListSterRev>')
    OR OPERTN_4_19 IN ('<ProcListSterRev>')
    OR OPERTN_4_20 IN ('<ProcListSterRev>')
    OR OPERTN_4_21 IN ('<ProcListSterRev>')
    OR OPERTN_4_22 IN ('<ProcListSterRev>')
    OR OPERTN_4_23 IN ('<ProcListSterRev>')
    OR OPERTN_4_24 IN ('<ProcListSterRev>'))

GROUP BY [FYEAR], [APPTAGE]