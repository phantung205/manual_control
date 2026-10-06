import pandas as pd
from configs import config_gas

def load_data():
    return pd.read_csv(config_gas.path_data_gas)

def clear_raw_data(df,is_train=True):
    df = df.copy()

    if is_train:
        #  xóa các cột có dữ liệu trung lặp
        df = df.drop_duplicates()
        # thêm cột mới
        df['MQ2_Analog'] = (df['Raw H2'] + df['Raw Ethanol']) / 2

        # dữ lại các cột cần
    if is_train:
        required_cols = (
                config_gas.numerical_col +
                config_gas.target_col
        )
        df = df[required_cols]
    else:
        df = df[config_gas.numerical_col]

    return df


if __name__ == '__main__':
    df = load_data()
    df_test = clear_raw_data(df)