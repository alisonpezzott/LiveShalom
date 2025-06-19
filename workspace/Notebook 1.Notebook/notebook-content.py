# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "cbf78fa8-e014-4255-80f7-29f7b3e3d5fa",
# META       "default_lakehouse_name": "Lake01",
# META       "default_lakehouse_workspace_id": "f74dee6c-66ce-4099-9c31-d0f481e36f59",
# META       "known_lakehouses": [
# META         {
# META           "id": "cbf78fa8-e014-4255-80f7-29f7b3e3d5fa"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import os 
import pandas as pd
from pyspark.sql.functions import split, explode, col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Definições
lake_path = "abfss://LiveShalom@onelake.dfs.fabric.microsoft.com/Lake01.Lakehouse"
raw_filename = "Microsoft MVP CPLP.xlsx"
file_path = lake_path + "/Files/Raw/" + raw_filename

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Lendo com pandas
pandas_df = pd.read_excel(file_path, engine="openpyxl")
display(pandas_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Quebrando em linhas as categorias
df = spark.createDataFrame(pandas_df)

df = df.selectExpr(
    "Nome",
    "`Gênero` as Genero",
    "`País` as Pais",
    "explode(split(Categoria, ', ')) as Categoria"
)
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Salvando nos arquivos
cleaned_file = "mvps_cplp.parquet"
cleaned_file_path = lake_path + "/Files/Cleaned/" + cleaned_file
os.makedirs(lake_path + "/Files/Cleaned", exist_ok=True)
df.write.parquet(cleaned_file_path, mode="overwrite")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Salvando nas tabelas
table_name = "mvps_cplp"
table_path = lake_path + "/Tables/" + table_name  
df.write.format("delta").mode("overwrite").option("overwriteSchema","True").save(table_path)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
