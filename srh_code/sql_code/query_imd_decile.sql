SELECT [RANK_LSOA] as IMD_rank
      ,[QUANTILE_DESC] as IMD_decile
  FROM [<Database>].[schema].[<Table>]
  WHERE [YEAR_LSOA] = <Year> AND
  [QUANTILE_TYPE] = 'Decile'