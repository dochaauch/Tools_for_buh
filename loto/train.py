import random
import pandas as pd
import numpy as np
import ast
from keras.models import Sequential
from keras.layers import LSTM, Dense

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor

from sklearn.metrics import accuracy_score



def read_dataset_from_csv(file_path):
    data = pd.read_csv(file_path)
    return data


def divide_to_train_and_test(df):
    # Divide the data into training and testing sets
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    return train_data, test_data




def main():
    file_path = '/Users/docha/PycharmProjects/Tools_for_buh/loto/eurojackpot_results.csv'
    df = read_dataset_from_csv(file_path)
    print(df.to_string)
    train_data, test_data = divide_to_train_and_test(df)
    print(train_data)



if __name__ == "__main__":
    main()

