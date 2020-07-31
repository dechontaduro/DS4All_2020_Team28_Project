App
+ app.py: frontend de la App.
Utiliza los siguientes datasets:
- /data/matrix/matrix_consol_v2.zip: registros mensuales consolidados de las variables para hacer el forecast y las gráficas exploratorias.
- /model/forecast.csv: predicciones mensuales de la variable de caudal para los diferentes modelos.
- /model/model_rank.csv: ranking de los modelos por macrocuenca de acuerdo al nivel de accuracy.

Scripts
Obtain: scripts enfocados en obtener los datasets para el análisis.
\obtain\ideam_scraping.py: Scrapping de las diferentes variables del IDEAM.
\obtain\unir_csv.py: Unificar las variables de un mismo tipo generadas a partir de diferentes tipos de estaciones.

Scrub: scripts para la limpieza o la conversión de formatos:
\scrub\ConvertShape2GeoJSON.ipynb: Convertir mapas en formato SHAPE a formato GeoJSON.
\scrub\CuencaCompletitud.ipynb: Determinar cuales estaciones tienen al menos el 70% de completitud de los datos para incluirse en el análisis.
\scrub\EstacionesIDEAM.ipynb: Preparar el dataset de las estaciones del IDEAM para las cuales se hará scrapping.
\scrub\lossCoverMonthMatrix.ipynb: Convertir la variable de loss cover de formato anual a mensual
\scrub\Preparar_VariableCaudalMedio.ipynb
\scrub\Preparar_VariableTemperaturaMedia.ipynb
\scrub\PromedioPonderaco_PTPM_CON_M.ipynb
\scrub\RevisionDatosCaudal.ipynb
\scrub\RevisionDatosTemperatura.ipynb
\scrub\VariableAjustarFormatoFecha.ipynb
\scrub\VariablesSplitFromScrappings.ipynb

Explore: scripts enfocados a explorar los diferentes datasets.
\scrub\EstacionesIDEAM_DatosPerfil.ipynb: 
\scrub\EstacionesVerificarCompletitud.ipynb
\explore\Clustering_v1.ipynb
\explore\Clustering_v2.ipynb
\explore\EDA_colombia_boxplot.ipynb
\explore\EDA_Decompose_Time_Series.ipynb
\explore\EDA_Describe_NaN_GeoMaps.ipynb
\explore\EDA_Macrocuenca.ipynb
\explore\EDA_merge_IDEAM_FCL.ipynb
\explore\EstacionesCompletasUnificar.ipynb
\explore\VariableAgregarPorMes.ipynb
\explore\VariableAgrupacionesVerificaciones.ipynb
\explore\VariableConsolidate.ipynb
\explore\VariableConsolidateV2.ipynb
\explore\VariableImputacion.ipynb
\explore\VariableImputacion2.ipynb
\explore\VariableMensualCompletarVariablesCuenca.ipynb
\explore\VariableMensualTop5PlotLine.ipynb
\explore\VariableMensualTop5Plots.ipynb
\explore\VariableMensualUnificar.ipynb
\explore\VariableMensualUnificar2_nousada.ipynb
\explore\VariablePivot.ipynb
\explore\VariablePorMesExploracion.ipynb
\explore\VariableQuitarOutliers.ipynb
\explore\VariablesMensualesUnificadaFiltrar.ipynb

\model\LSTM.ipynb
\model\Multivariate_time_series_forecasting.ipynb
\model\Multivariate_time_series_Random_Forest.ipynb
\model\Multivariate_time_series_VECM.ipynb
\model\Multivariate_time_series_XGBoost.ipynb
\model\VAR.ipynb

\libs\process_files.py
\model\coint_johansen.py
