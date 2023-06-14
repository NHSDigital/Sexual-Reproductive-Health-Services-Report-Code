/*
Site code and name are renamed to match SRHAD extract names
*/

SELECT [CODE] as ClinicID
      ,[NAME] as [CLINIC NAME]
      ,[POSTCODE]  as [CLINIC POSTCODE]
      ,[OPEN_DATE] as Open_date
  FROM [<Database>].[schema].[<Table>]
ORDER BY ClinicID, Open_date