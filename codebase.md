![DS4A2020](/FrontEnd/assets/img/DS4A.svg)

# IMPACT OF FOREST COVER LOSS ON RIVER FLOW REGIME IN COLOMBIA
+ **\FrontEnd\app.py**: frontend.

Use the following datasets:
1. **\data\matrix\matrix_consol_v2.zip**: monthly consolidated records of the variables to make the forecast and exploratory graphs.
2. **\model\forecast.csv**: monthly predictions of the flow variable for the different models.
3. **\model\model_rank.csv**: ranking of the models by macro basin according to the level of accuracy.

# Scripts
## Obtain: scripts focused on obtaining datasets for analysis.
- **\obtain\ideam_scraping.py**: Scrapping of the different IDEAM variables.
- **\obtain\unir_csv.py**: Unify variables of the same type generated from different types of stations.

## Scrub: scripts for cleanup, format conversion, and preparation for exploration and modeling.
- **\scrub\EstacionesIDEAM.ipynb**: Prepare the dataset of the IDEAM stations for which it will be scrapping.
- **\scrub\VariableAjustarFormatoFecha.ipynb**: Adjust the date format for some records that differ from the general format.
- **\scrub\VariablesSplitFromScrappings.ipynb**: Separate the records by type of variables because when they are downloaded from the IDEAM they are mixed in a single file per type of station.
- **\explore\VariableMensualUnificar.ipynb**: Unify the monthly records of the variables in a single dataset in short format. Additionally, create the wide format of this dataset.
- **\explore\EstacionesCompletasUnificar.ipynb**: Unification of the stations with completeness in variables of 70% minimum.
- **\scrub\CuencaCompletitud.ipynb**: Determine which stations have at least 70% completeness of the data to be included in the analysis.
- **\scrub\ConvertShape2GeoJSON.ipynb**: Convert maps in SHAPE format to GeoJSON format.
- **\scrub\lossCoverMonthMatrix.ipynb**: Convert loss cover variable from annual to monthly format.
- **\explore\EDA_merge_IDEAM_FCL.ipynb**: Prepare the variable forest cover loss for each basin.
- **\explore\VariableAgregarPorMes.ipynb**: summarizes the variables by month by station, generating the minimum, average, median and maximum value of the daily records.
- **\explore\VariablesMensualesUnificadaFiltrar.ipynb**: Unification of the monthly variables and filtering for the time range of the analysis.
- **\explore\VariableConsolidate.ipynb**: Consolidation of all variables in a single dataset in wide format.
- **\explore\VariableConsolidateV2.ipynb**: Consolidation of all variables in a single dataset in wide format. Version 2.
- **\explore\VariableQuitarOutliers.ipynb**: Remove the outliners from the series.

## Explore: scripts focused on exploring different datasets.
- **\scrub\EstacionesIDEAM_DatosPerfil.ipynb**: Heatmaps with the number of annual and monthly records for each station and for each of the variables.
- **\scrub\EstacionesVerificarCompletitud.ipynb**: Calculation of the number of stations with at least 70% of daily registration in each of the years of the analysis.
- **\explore\Clustering_v1.ipynb**: Cluster analysis for each of the basins.
- **\explore\Clustering_v2.ipynb**: Cluster analysis for each of the basins. Version 2.
- **\explore\EDA_colombia_boxplot.ipynb**: exploratory boxplot graph for each of the variables per month without discriminating by basin.
- **\explore\EDA_Decompose_Time_Series.ipynb**: Decomposition of the time series for each basin and for each variable.
- **\explore\EDA_Describe_NaN_GeoMaps.ipynb**: Display of geographically empty records.
- **\explore\EDA_Macrocuenca.ipynb**: exploratory boxplot, timeseries and correlation graphs for the selected basins.
- **\explore\VariableImputacion.ipynb**: Fill in the value of the day with the median of the values ​​that were held for the same day and month throughout the range and only if there are at least 10 years
- **\explore\VariableMensualTop5PlotLine.ipynb**: Time series graphs of the 5 basins with the highest and lowest flow.
- **\explore\VariableMensualTop5Plots.ipynb**: Boxplot graphs of the 5 basins with the highest and lowest flow.
- **\explore\VariablePorMesExploracion.ipynb**:  Monthly exploratory graphs of the variables.

## Model: scripts for creating the models
- **\model\LSTM.ipynb**: Training and validation of the LSTM model for flow.
- **\model\LSTM_forecast_2020_2021.ipynb**: Generate flow predictions using the LSTM model.
- **\model\VAR.ipynb**: Training and validation of the LSTM model for flow.
- **\model\VAR_forecast_2020_2021.ipynb**: Generate flow predictions using the VAR model.
- **\model\Multivariate_time_series_Random_Forest.ipynb**: Training and validation of the Random Forest model for flow.
- **\model\Multivariate_time_series_VECM.ipynb**: Training and validation of the VECM model for flow.
- **\model\Multivariate_time_series_XGBoost.ipynb**: Training and validation of the XGBoost model for flow.
- **\model\Multivariate_time_series_forecasting.ipynb**: Training and validation of the LSTM model for flow.

## Libs: general functionality scripts
- **\libs\process_files.py**: Apply a function to the files in a path
