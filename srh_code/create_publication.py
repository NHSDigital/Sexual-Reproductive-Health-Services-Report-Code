import time
import timeit
import logging
from srh_code.utilities import logger_config
import srh_code.parameters as param
from srh_code.utilities import helpers
from srh_code.utilities import tables, charts, maps
import srh_code.utilities.publication_files as publication
from srh_code.utilities.write import write_data
from srh_code.utilities import load, pre_processing
import xlwings as xw


def main():

    # Created a temp folder for storing cached dataframes
    # (will be removed at end).
    helpers.create_folder("cached_dataframes/")

    # Load parameters

    # Load reporting financial year
    fyear = param.FYEAR
    # Derive last full calendar year from financial year (for prescribing data)
    cyear = int(fyear[:4])
    # Load template/main file location parameters
    tables_template = param.TABLE_TEMPLATE
    charts_template = param.CHART_TEMPLATE
    prescribing_path = param.PRESCRIBING_PATH
    prescribing_ref_path = param.PRESCRIBING_REF_PATH
    maps_template = param.MAP_TEMPLATE
    # Load run parameters
    run_tables_srhad = param.RUN_TABLES_SRHAD
    run_tables_prescribing = param.RUN_TABLES_PRESCRIBING
    run_tables_ahas = param.RUN_TABLES_AHAS
    run_charts_srhad = param.RUN_CHARTS_SRHAD
    run_charts_prescribing = param.RUN_CHARTS_PRESCRIBING
    run_charts_ahas = param.RUN_CHARTS_AHAS
    run_maps_srhad = param.RUN_MAPS_SRHAD
    run_pub_outputs = param.RUN_PUBLICATION_OUTPUTS
    # Load the expected column content for the external import files
    cols_prescribing_source = param.PRESCRIBING_SOURCE_COLS
    cols_prescribing_ref = param.PRESCRIBING_REF_COLS

    # Run each part of the pipeline as per the run flags

    # Run the data imports and pre-processing
    if run_tables_srhad or run_charts_srhad or run_tables_ahas or run_charts_ahas or run_maps_srhad:
        # Import LA reference data for the current period and
        # apply pre-processing updates. Add to cache for later use.
        df_org_ref = pre_processing.create_la_ref_data()
        df_org_ref.to_feather('cached_dataframes/df_la_ref.ft')

        # Import the old to new LSOA lookup
        df_lsoa_ref = load.import_lsoa_ref()
        # Import and process the IMD reference data (LSOA to IMD decile lookup)
        df_imd_ref = pre_processing.create_imdref_data()
        # Import and process population data. Add to cached folder
        df_pop = load.import_population_data()
        df_pop = pre_processing.update_population_data(df_pop,
                                                       df_org_ref,
                                                       df_imd_ref)
        df_pop.to_feather("cached_dataframes/df_pop.ft")

        # Import the srhad source data
        df_srhad = load.import_reporting_table_data()
        # Run pre-processing updates on the srhad data
        df_srhad = pre_processing.update_srhad_source_data(df_srhad,
                                                           df_org_ref,
                                                           df_lsoa_ref,
                                                           df_imd_ref,
                                                           fyear)

        if run_tables_ahas or run_charts_ahas:
            # Import the ahas source data (for sterilisation & vasectomy outputs)
            df_ahas = load.import_ahas_vas_ster_data()
            # Run pre-processing on the sterilisation & vasectomy data (srhad and ahas)
            df_ster_vas = pre_processing.create_ster_vas_data(df_srhad, df_ahas)

    # Run prescribing imports and pre-processing
    if run_tables_prescribing or run_charts_prescribing:
        # Import the prescribing source data and reference data files.
        df_prescribing = load.import_from_excel(prescribing_path,
                                                "srh_prescribing_source",
                                                cols_prescribing_source)
        df_pres_ref = load.import_from_excel(prescribing_ref_path,
                                             "srh_prescribing_reference",
                                             cols_prescribing_ref)
        # Run pre-processing updates on the prescribing data
        df_prescribing = pre_processing.update_prescribing_data(df_prescribing,
                                                                df_pres_ref,
                                                                cyear)

    if run_tables_srhad:
        # Run the SRHAD tables as defined by the items in get_tables_shrad
        all_tables = tables.get_tables_srhad()
        write_data.write_outputs(df_srhad, all_tables, tables_template,
                                 fyear)

    if run_tables_prescribing:
        # Run the prescribing tables as defined by the items in get_tables_prescribing
        all_tables = tables.get_tables_prescribing()
        write_data.write_outputs(df_prescribing, all_tables, tables_template,
                                 cyear)

    if run_tables_ahas:
        # Run the AHAS tables as defined by the items in get_tables_ahas
        all_tables = tables.get_tables_ahas()
        write_data.write_outputs(df_ster_vas, all_tables, tables_template,
                                 fyear)

    # If any table content was updated, than save the Excel master tables
    # with the updated data and close Excel
    if run_tables_srhad or run_tables_prescribing or run_tables_ahas:
        wb = xw.Book(tables_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_charts_srhad:
        # Run the srhad chart outputs as defined by the items in get_charts_srhad
        all_charts = charts.get_charts_srhad()
        write_data.write_outputs(df_srhad, all_charts, charts_template,
                                 fyear)

    if run_charts_ahas:
        # Run the AHAS chart outputs as defined by the items in get_charts_ahas
        all_charts = charts.get_charts_ahas()
        write_data.write_outputs(df_ster_vas, all_charts, charts_template,
                                 fyear)

    if run_charts_prescribing:
        # Run the srhad chart outputs as defined by the items in get_charts_srhad
        all_charts = charts.get_charts_prescribing()
        write_data.write_outputs(df_prescribing, all_charts, charts_template,
                                 cyear)

    # If any chart content was updated, than save the Excel master tables
    # with the updated data and close Excel
    if run_charts_srhad or run_charts_prescribing or run_charts_ahas:
        wb = xw.Book(charts_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_maps_srhad:
        # Run the map tables as defined by the items in get_maps_srhad
        all_maps = maps.get_maps_srhad()
        write_data.write_outputs(df_srhad, all_maps, maps_template, fyear)
        wb = xw.Book(maps_template)
        wb.save()
        xw.apps.active.api.Quit()

    # Save the cms ready tables and chart files to the publication area
    if run_pub_outputs:
        publication.save_tables(tables_template)
        publication.save_charts_as_image(charts_template)

    # Remove the cached dataframe folder and all it's contents
    helpers.remove_folder("cached_dataframes/")


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" / f"srh_serives_create_pub_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_publication: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)
