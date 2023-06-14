SELECT [<LSOAField>] as Org_code
      ,[RANK_IMD] as IMD_rank
  FROM [<Database>].[schema].[<Table>]
  WHERE [IMD_YEAR] = <Year>