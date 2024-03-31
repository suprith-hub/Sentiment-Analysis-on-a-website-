import os

import pandas as pd


def create_output_csv_file():
    # Get the absolute path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the absolute path to the Excel file
    excel_file_path = os.path.join(script_dir, '..', 'Output Data Structure.xlsx')
    df = pd.read_excel(excel_file_path)
    attributes = df.columns.tolist()


    with open('output.csv', 'w') as f:
        f.write(','.join(attributes) + '\n')