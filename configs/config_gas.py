import os
from configs import path_common


# directory data
dir_data_gas_raw = os.path.join(path_common.dir_raw_data,"gas_warning")

path_data_gas = os.path.join(dir_data_gas_raw,"smoke_detection_iot.csv")


# required columns
target_col = ["Fire Alarm"]
numerical_col = ["Temperature[C]","Humidity[%]","MQ2_Analog"]
