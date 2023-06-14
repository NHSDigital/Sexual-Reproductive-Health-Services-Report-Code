/*
Creates population counts by the alternate age groupings (13 to 54) needed for
the population rates (age group field name should match that created by the
create_age_groups_alt function in 'field_definitions.py'.
Data is aggregated at this stage due to the large number of rows represented
by LSOA level data.

*/

WITH AgeGroupData As
(SELECT [GENDER] as Gender
    ,[YEAR_OF_COUNT]
    ,[GEOGRAPHIC_SUBGROUP_CODE] as Org_code
    ,[ONS_RELEASE_DATE] as Release_date
    ,[POPULATION_COUNT] as Population
    ,CASE
             WHEN [AGE_LOWER] BETWEEN 13 AND 14 THEN '13-14'
             WHEN [AGE_LOWER] = 15 THEN '15'
             WHEN [AGE_LOWER] BETWEEN 16 AND 17 THEN '16-17'
             WHEN [AGE_LOWER] BETWEEN 18 AND 19 THEN '18-19'
             WHEN [AGE_LOWER] BETWEEN 20 AND 24 THEN '20-24'
             WHEN [AGE_LOWER] BETWEEN 25 AND 34 THEN '25-34'
             WHEN [AGE_LOWER] BETWEEN 35 AND 44 THEN '35-44'
             WHEN [AGE_LOWER] BETWEEN 45 AND 54 THEN '45-54'
       END                                            AS Age_group_alt
FROM [<Database>].[schema].[<Table>]
WHERE 
[AGE_LOWER] between 13 and 54
AND
(([YEAR_OF_COUNT] = <YearOfCount> AND
[GEOGRAPHIC_GROUP_CODE] in ('E06','E08','E09','E10','E12','E92'))
OR
([YEAR_OF_COUNT] = <YearOfCountLSOA> AND [GEOGRAPHIC_GROUP_CODE] = 'E01'))
)
SELECT Org_code 
    ,Gender
    ,Age_group_alt
    ,Release_date
    ,sum(Population) as Count
FROM AgeGroupData
GROUP BY Org_code, Gender, Age_group_alt, Release_date
ORDER BY Org_code, Release_date
