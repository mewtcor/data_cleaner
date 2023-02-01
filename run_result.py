#!/usr/bin/env python

import pandas as pd

df = pd.read_csv("run_results.csv")
print(df.columns)
prefix = input('type the column prefix (ex. data_product_code prefix is "data_"): ')

has_tmp = df.columns.str.contains('tmp').any()
if has_tmp:
    count_tmp_cols = df.filter(regex='tmp', axis=1).shape[1]
    print(f'total tmp cols: {count_tmp_cols}')
    df = df.filter(regex='^(?!.*tmp.*)')
    print('tmp cols deleted')
else:
    print("dataframe does nofrom openpyxl import Workbook have any columns with keyword 'tmp'")

if 'remove' in df.columns:
    count_remove_cols = df.filter(like='remove', axis=1).shape[1]
    print(f'total remove cols: {count_remove_cols}')
    df = df.drop(columns=["remove"])
    print('remove cols deleted')
else:
    print("The column 'remove' does not exist in the dataframe.")

if 'flag' in df.columns:
    count_flag_cols = df.filter(like='flag', axis=1).shape[1]
    print(f'total flag cols: {count_flag_cols}')
    df = df.drop(columns=["flag"])
    print('flag cols deleted')
else:
    print("The column 'flag' does not exist in the dataframe.")

df = df.rename(columns=lambda x: x.replace(prefix, "")) # column header prefix cleaning
null_rows = df[df["product_code"].isnull()]
data_without_nulls = df.dropna(subset=["product_code"])
# data_without_nulls.to_csv("data_with_product_codes.csv", index=False)
duplicate_rows = data_without_nulls[data_without_nulls.duplicated(subset=["product_code"], keep=False)]
data_without_duplicates = data_without_nulls.drop_duplicates(subset=["product_code"], keep='first')
columns_order = ["product_code", "product_name", "category1", "category2", "description", "image1", "pageUrl"]
data_without_duplicates = data_without_duplicates.reindex(columns=columns_order + list(set(data_without_duplicates.columns) - set(columns_order)))

num_columns = len(df.columns)
print(f'total columns: {num_columns}')
total_null_rows = len(null_rows.index)
print(f'number of rows with empty product codes: {total_null_rows}')
total_dup_rows = len(duplicate_rows.index)
print(f'number of duplicate rows: {total_dup_rows}')
total_rows_after_cleaning = len(data_without_duplicates.index)
print(f'total products after cleaning: {total_rows_after_cleaning}')

null_rows.to_csv("null_product_codes.csv", index=False)
duplicate_rows.to_csv("duplicates.csv", index=False)
data_without_duplicates.to_csv("data_without_duplicates_and_nulls.csv", index=False)

# data_without_duplicates.to_parquet("data_without_duplicates_and_nulls.parquet", index=False)


