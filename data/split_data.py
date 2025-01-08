import pandas as pd
import os


def split_data_into_halves(directory, filename, file_format=".csv"):
    input_path = os.path.join(directory, filename + file_format)
    df = pd.read_csv(input_path)
    mid = len(df) // 2
    df1 = df.iloc[:mid]
    df2 = df.iloc[mid:]
    df1.to_csv(os.path.join(directory, filename + "_1" + file_format), index=False)
    df2.to_csv(os.path.join(directory, filename + "_2" + file_format), index=False)
    os.remove(input_path)
    
def main():
    directories = ["airbnb", "air_quality", "sales", "geo"]
    filenames = ["ab_nyc", "air_quality", "nyc_rolling_sales", "NHoodNameCentroids"]
    
    for directory, filename in zip(directories, filenames):
        split_data_into_halves(directory, filename)


if __name__ == "__main__":
    main()