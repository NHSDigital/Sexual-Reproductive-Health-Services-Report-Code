"""
Purpose of the script: contains the Excel automation script.
"""
import pandas as pd
import xlwings as xw
import xlsxwriter
from srh_code.utilities import helpers
from srh_code.utilities.write import write_format
import srh_code.utilities.processing.processing_publication as processing
import logging


def write_to_excel_static(df, output_path, sheetname, write_cell,
                          include_row_labels=False, empty_cols=None):
    """
    Write data to an excel template. Assumes the table length remains constant.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section seperator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.

    Returns
    -------
    None
    """

    logging.info("Writing data to specified output file")

    # If row labels are required then reset the index so that they are included
    # when writing values (assumes index contains row labels)
    if include_row_labels:
        df.reset_index(inplace=True)

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = write_format.insert_empty_columns(df, empty_cols, write_cell)

    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # write to the specified cell
    sht.range(write_cell).value = df.values


def write_to_excel_variable(df, output_path, sheetname, write_cell,
                            include_row_labels=False, empty_cols=None):
    """
    Write data to an excel template. Can accommodate dataframes where the
    number of rows may change e.g. LA data where the number of LAs may change
    each year.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
        This should be the first cell in the master file where the variable
        data currently exists as it also determines which row to delete first
        e.g. for LAs would be the first cell of the first row of LA data
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section seperator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.
    Returns
    -------
    None
    """

    logging.info("Writing data to specified output file")

    # If row labels are required then reset the index so that they are included
    # when writing values (assumes index contains row labels)
    if include_row_labels:
        df.reset_index(inplace=True)

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = write_format.insert_empty_columns(df, empty_cols, write_cell)

    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Get Excel row number of write cell
    firstrownum = helpers.excel_cell_to_row_num(write_cell)

    # Get Excel row number of last row of existing data
    lastrownum_current = sht.range(write_cell).end('down').row

    # Clear all existing data rows from write_cell to end of data
    delete_rows = str(firstrownum) + ":" + str(lastrownum_current)
    sht.range(delete_rows).delete()

    # Count number of rows in dataframe
    df_rowcount = len(df)

    # Create range for new set of rows and insert into sheet
    lastrownnum_new = firstrownum + df_rowcount - 1
    df_rowsrange = str(firstrownum) + ":" + str(lastrownnum_new)

    sht.range(df_rowsrange).insert(shift='down')

    # Write dataframe to the Excel sheet starting at the write_cell reference
    sht.range(write_cell).value = df.values


def write_to_excel_with_headers(df, output_path, sheetname, write_cell,
                                header_cell, include_row_labels=False,
                                empty_cols=None):
    """
    Write data to an excel template including dataframe column headers, where
    the number of columns is variable.
    Assumes the table length remains constant.

    Parameters
    ----------
    df : pandas.DataFrame
    output_path : path
        Filepath of the Excel file that the data will be written to.
    sheetname : str
        Name of the destination Excel worksheet.
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data)
    header_cell: str
        identifies the cell location in the Excel worksheet where the header
        values will be pasted (leftmost position of header row)
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section seperator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Default is None.

    Returns
    -------
    None
    """

    logging.info("Writing data to specified output file")

    # If row labels are required then reset the index so that they are included
    # when writing values (assumes index contains row labels)
    if include_row_labels:
        df.reset_index(inplace=True)

    # Add empty columns where present in target Excel worksheet
    if empty_cols is not None:
        df = write_format.insert_empty_columns(df, empty_cols, write_cell)

    # Load the template and select the required table sheet
    wb = xw.Book(output_path)
    sht = wb.sheets[sheetname]
    sht.select()

    # Get first and last Excel column numbers of existing data
    firstcolnum = helpers.excel_cell_to_col_num(write_cell)
    lastcolnum = sht.range(write_cell).end('right').last_cell.column
    # Convert to Excel letters
    firstcol = xlsxwriter.utility.xl_col_to_name(firstcolnum - 1)
    lastcol = xlsxwriter.utility.xl_col_to_name(lastcolnum - 1)

    # Clear all columns from write_cell to end of existing data
    delete_cols = firstcol + ":" + lastcol
    sht.range(delete_cols).delete()

    # Check the number of columns in the data to be pasted (minus the index)
    df_cols = len(df.columns) - 1
    # Use this to set the new Excel column range to be inserted
    lastcolnum_new = firstcolnum + df_cols + 1
    lastcol_new = xlsxwriter.utility.xl_col_to_name(lastcolnum_new - 1)
    insert_cols = firstcol + ":" + lastcol_new

    # Insert the empty columns that will hold the new data. This method ensures
    # that the preset formatting to the left of the first new column is applied
    # across the new range.
    sht.range(insert_cols).insert(shift='right')

    # Extract the headers to be pasted and paste them into the header write cell
    headers = df.columns.values
    sht.range(header_cell).value = headers

    # Paste the dataframe values into the write cell
    sht.range(write_cell).value = df.values

    # Apply the table specific re-formatting required for this type of table
    # (due to removal of labels / formats etc. during column deletion}
    write_format.excel_table_specific_formatting(output_path, sheetname,
                                                 write_cell)


def write_csv(df, output_path, output_name, index=True):
    """
    Writes a dataframe to a csv

    Parameters
    ----------
    df :pandas.DataFrame
    output_path: Path
        Folder path where output will be written.
    output_name: str
        Name to be asssigned to output file name.
    index: bool
        Include index in output. Set to True by default.

    Returns
    -------
    .csv file

    """
    # Set full file path / name
    file_name = output_name + ".csv"
    save_path = output_path / file_name

    # Save dataframe to csv
    df.to_csv(save_path, index=index)


def select_write_type(df, write_type, output_path, output_name,
                      write_cell, header_cell=None, include_row_labels=False,
                      empty_cols=None):
    """
    Determines which type of write function is needed and performs that
    function.

    Parameters
    ----------
    df :pandas.DataFrame
    write_type: str
        Determines the method of writing the output.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    output_name: str
        Name of the worksheet to be written to (for Excel) or to be asssigned
        as the name of the output file (for csv's).
    write_cell: str
        identifies the cell location in the Excel worksheet where the data
        will be pasted (top left of data). Not required if the write_type is
        csv.
    header_cell: str
        identifies the cell location in the Excel worksheet where the header
        values will be pasted (leftmost position of header row).
        Only required for write_type = excel_with_headers.
    include_row_labels: bool
        Determines if the row labels will be written.
    empty_cols: list[str]
        A list of letters representing any empty (section seperator) excel
        columns in the worksheet. Empty columns will be inserted into the
        dataframe in these positions. Not required if the write_type is
        csv.

    Returns
    -------
    .csv file

    """
    # Check for invalid write_type agrument
    valid_values = ["csv", "excel_static", "excel_variable",
                    "excel_with_headers"]
    helpers.validate_value_with_list("write_type", write_type, valid_values)

    # Choose the write method based on write_type
    if write_type == "csv":
        write_csv(df, output_path, output_name)
    elif write_type == "excel_variable":
        write_to_excel_variable(df, output_path, output_name,
                                write_cell, include_row_labels, empty_cols)
    elif write_type == "excel_with_headers":
        write_to_excel_with_headers(df, output_path, output_name, write_cell,
                                    header_cell, include_row_labels, empty_cols)
    else:
        write_to_excel_static(df, output_path, output_name,
                              write_cell, include_row_labels, empty_cols)


def write_outputs(df, output_args, output_path, year):
    """
    Processes and writes the data for each function to the output location
    as defined by parameters taken from the output_args dictionary.

    Parameters
    ----------
    df :pandas.DataFrame
    output_args: list[dict]
        Provides all the required arguments needed to run and write each
        output.
    output_path: Path
        Path where output will be written. Full file path if writing to Excel
        or the folder path if writing to a csv.
    year: str
        The current reporting year value that will be used if required by the
        write process (time series tables only).
    not_applicable: str

    Returns
    -------
    None

    """
    # For each item in the output_args dictionary
    for output in output_args:
        # Extract all the required arguments from the output_args dictionary
        # Some arguments are not needed if the write_type is csv
        name = output["name"]
        write_type = output["write_type"]

        if write_type == "csv":
            write_cell = None
            header_cell = None
            include_row_labels = None
            empty_cols = None
            year_check_cell = None
            years_as_rows = None
        else:
            write_cell = output["write_cell"]
            include_row_labels = output["include_row_labels"]
            empty_cols = output["empty_cols"]
            year_check_cell = output["year_check_cell"]
            years_as_rows = output["years_as_rows"]
            # header_cell only applicable for write_type excel_with_headers
            if write_type == "excel_with_headers":
                header_cell = output["header_cell"]
            else:
                header_cell = None

        # Run the function(s) in the dictionary item(s) beginning with 'contents'.
        # Where there are multiple functions in the contents for one output,
        # the returned dataframes are concatenated. For unmatched columns null
        # values will be created.
        # Where there are multiple contents keys, the outputs will be concatenated
        # along columns (same identical length is assumed on contents set up).
        # List to store the different outputs to join
        total_dfs = []
        # Check the output dictionary for keys starting with contents
        keys = list(output.keys())
        content_keys = [key for key in keys if key.startswith("contents")]
        for content_key in content_keys:
            logging.info(f"Running {content_key} for {name}")
            df_content = pd.concat([content(df) for content in output[content_key]])
            total_dfs.append(df_content)

        # Where there was more than one contents key then these are joined
        # along columns (on index).
        df_output = pd.concat(total_dfs, axis=1).fillna(0)

        # Perform any final updates to the dataframe for specific outputs
        df_output = processing.output_specific_updates(df_output, name)

        # If a table outout contains fixed length time series data (year_check_cell
        # will be populated) then check if the time series in Excel needs preparing
        # (moving along one year).
        if year_check_cell is not None:
            write_format.check_latest_year(output_path, name,
                                           year_check_cell, year,
                                           years_as_rows)

        # Write the output as per the selected write type
        select_write_type(df_output, write_type, output_path,
                          name, write_cell, header_cell,
                          include_row_labels, empty_cols)
