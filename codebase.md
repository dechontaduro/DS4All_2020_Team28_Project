# App
+ **app.py**: frontend de la App.

Utiliza los siguientes datasets**:
1. **\data\matrix\matrix_consol_v2.zip**: registros mensuales consolidados de las variables para hacer el forecast y las gráficas exploratorias.
2. **\model\forecast.csv**: predicciones mensuales de la variable de caudal para los diferentes modelos.
3. **\model\model_rank.csv**: ranking de los modelos por macrocuenca de acuerdo al nivel de accuracy.

# Scripts
## Obtain: scripts enfocados en obtener los datasets para el análisis.
- **\obtain\ideam_scraping.py**: Scrapping de las diferentes variables del IDEAM.
- **\obtain\unir_csv.py**: Unificar las variables de un mismo tipo generadas a partir de diferentes tipos de estaciones.

## Scrub: scripts para la limpieza, conversión de formatos y preparación para la exploración y el modelamiento**:
- **\scrub\EstacionesIDEAM.ipynb**: Preparar el dataset de las estaciones del IDEAM para las cuales se hará scrapping.
- **\scrub\VariableAjustarFormatoFecha.ipynb**: Ajustar el formato de fecha para algunos registros que difieren en el formato general.
- **\scrub\VariablesSplitFromScrappings.ipynb**: Separar los registros por tipo de variables pues cuando se descargan del IDEAM vienen mezclados en un sólo archivo por tipo de estación
- **\explore\VariableMensualUnificar.ipynb**: Unificar los registros mensuales de las variables en un solo dataset en formato corto. Adicionalmente, crear el formato ancho de este dataset.
- **\explore\EstacionesCompletasUnificar.ipynb**: unificación de las estaciones con completitud en variables mínima del 70%
- **\scrub\CuencaCompletitud.ipynb**: Determinar cuales estaciones tienen al menos el 70% de completitud de los datos para incluirse en el análisis.
- **\scrub\ConvertShape2GeoJSON.ipynb**: Convertir mapas en formato SHAPE a formato GeoJSON.
- **\scrub\lossCoverMonthMatrix.ipynb**: Convertir la variable de loss cover de formato anual a mensual
- **\explore\EDA_merge_IDEAM_FCL.ipynb**: Preparar la variable forest cover loss por cada cuenca
- **\explore\VariableAgregarPorMes.ipynb**: se resumen las variables por mes por estación, generando el valor mínimo, promedio, mediana y máximo de los registros diarios.
- **\explore\VariablesMensualesUnificadaFiltrar.ipynb**: Unificación de las variables mensuales y filtrado para el rango de tiempo del análisis.
- **\explore\VariableConsolidate.ipynb**: Consolidación de todas las variables en un sólo dataset en formato ancho.
- **\explore\VariableConsolidateV2.ipynb**: Consolidación de todas las variables en un sólo dataset en formato ancho Versión 2.
- **\explore\VariableQuitarOutliers.ipynb**: Eliminar los outliners de las series.

- ???\scrub\Preparar_VariableCaudalMedio.ipynb
- ???\scrub\Preparar_VariableTemperaturaMedia.ipynb
- ???\scrub\PromedioPonderaco_PTPM_CON_M.ipynb
- ???\scrub\RevisionDatosCaudal.ipynb
- ???\scrub\RevisionDatosTemperatura.ipynb


## Explore: scripts enfocados a explorar los diferentes datasets.
- **\scrub\EstacionesIDEAM_DatosPerfil.ipynb**: Heatmaps con la cantidad de registros anuales y mensuales para cada estación y por cada una de las variables.
- **\scrub\EstacionesVerificarCompletitud.ipynb**: Cálculo de la cantidad de estaciones con al menos el 70% de registro diario en cada uno de los años del análisis.
- **\explore\Clustering_v1.ipynb**: Análisis de cluster para cada una de las cuencas.
- **\explore\Clustering_v2.ipynb**: Análisis de cluster para cada una de las cuencas Versión 2.
- **\explore\EDA_colombia_boxplot.ipynb**: gráfica exploratoria boxplot para cada una de las variables por mes sin discriminar por cuenca.
- **\explore\EDA_Decompose_Time_Series.ipynb**: Descomposición de las series de tiempo para cada cuenca y por cada variable.
- **\explore\EDA_Describe_NaN_GeoMaps.ipynb**: Visualización de los registros vacíos geográficamente.
- **\explore\EDA_Macrocuenca.ipynb**: gráficas exploratorias boxplot, timeseries y de correlación para las cuencas seleccionadas.
- **\explore\VariableImputacion.ipynb**: Se rellena el valor del día con la mediana de los valores que se tuvieron para el mismo día y mes en todo el rango y sólo si existen mínimo 10 años
- **\explore\VariableMensualCompletarVariablesCuenca.ipynb
- **\explore\VariableMensualTop5PlotLine.ipynb**: Gráficas de series de tiempo de las 5 cuencas con mayor y menor caudal.
- **\explore\VariableMensualTop5Plots.ipynb**: Gráficas de boxplot de las 5 cuencas con mayor y menor caudal.
- **\explore\VariablePorMesExploracion.ipynb**: Gráficas exploratorias mensuales de las variables.

## Model**: scripts para la creación de los modelos
- **\model\LSTM.ipynb**: Entrenamiento y validación del modelo LSTM para caudal.
- **\model\LSTM_forecast_2020_2021.ipynb**: Generar predicciones para caudal usando el modelo LSTM.
- **\model\VAR.ipynb**: Entrenamiento y validación del modelo LSTM para caudal.
- **\model\VAR_forecast_2020_2021.ipynb**: Generar predicciones para caudal usando el modelo VAR.
- **\model\Multivariate_time_series_Random_Forest.ipynb**: Entrenamiento y validación del modelo Random Forest para caudal.
- **\model\Multivariate_time_series_VECM.ipynb**: Entrenamiento y validación del modelo VECM para caudal.
- **\model\Multivariate_time_series_XGBoost.ipynb**: Entrenamiento y validación del modelo XGBoost para caudal.

- **\model\Multivariate_time_series_forecasting.ipynb**: Entrenamiento y validación del modelo LSTM para caudal.
- **\model\coint_johansen.py


## Libs**: scripts de funcionalidades generales
- **\libs\process_files.py: Aplicar a los archivos en un path una función
