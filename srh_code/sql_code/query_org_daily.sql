/*
Org code and name are renamed to match SRHAD extract names
*/

SELECT [ORG_CODE] as OrganisationID
      ,[NAME] as [ORG NAME]
      ,[BUSINESS_START_DATE] as Open_date
FROM [<Database>].[schema].[<Table>]
ORDER BY OrganisationID, Open_date