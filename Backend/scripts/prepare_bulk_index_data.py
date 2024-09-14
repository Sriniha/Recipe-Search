import pandas as pd # type: ignore
import json

def prepare_bulk_data():
    # Load the .csv file
    csv_file = r"D:\sriansh\Recipes Search Platform\epi_r.csv"
    data = pd.read_csv(csv_file)

    # Convert fields that are meant to be integers
    def convert_floats_to_int(df):
        for column in df.columns:
            if df[column].dtype == 'float64':
                df[column] = df[column].fillna(0)
                if df[column].apply(lambda x: x.is_integer() if pd.notnull(x) else True).all():
                    df[column] = df[column].astype('int64')
        return df

    # Apply the conversion
    data = convert_floats_to_int(data)

    # Create the bulk index file
    json_file_path = r"D:\sriansh\Recipes Search Platform\epi_r_bulk.json"
    with open(json_file_path, 'w') as f:
        for i, (_, row) in enumerate(data.iterrows(), start=1):
            index_line = { "index": { "_index": "epi_r_index", "_id": str(i) } }
            f.write(json.dumps(index_line) + '\n')
            f.write(row.to_json() + '\n')

    print("Bulk file created successfully!")
    return json_file_path

if __name__ == "__main__":
    prepare_bulk_data()