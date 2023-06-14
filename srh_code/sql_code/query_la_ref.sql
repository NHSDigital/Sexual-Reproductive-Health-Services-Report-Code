SELECT [GEOGRAPHY_CODE] as Org_code
      ,[GEOGRAPHY_NAME] as Org_name
      ,[PARENT_GEOGRAPHY_CODE] as Parent_code
      ,[ENTITY_CODE] as Entity_code      
      ,[DATE_OF_OPERATION] as Open_date
  FROM [<Database>].[schema].[<Table>]
  WHERE [ENTITY_CODE] in ('E06','E07','E08','E09','E10','E12')
  AND ([DATE_OF_OPERATION] <= '<FYEnd>' AND ([DATE_OF_TERMINATION] IS NULL
  OR [DATE_OF_TERMINATION] >= '<FYStart>'))
ORDER BY Org_code, Open_date