import pandas as pd
import ast
import json


def safe_eval(x):
    if pd.isna(x):
        return []
    try:
        return ast.literal_eval(x)
    except (ValueError, SyntaxError):
        try:
            return json.loads(x)
        except json.JSONDecodeError:
            return [x] if x else []


def csv_to_excel(df, output_excel):
    # Convert string representations of lists to actual lists
    list_columns = ["emails", "digifabster_urls", "3yourmind_urls", "amfg_urls"]
    for col in list_columns:
        df[col] = df[col].apply(safe_eval)

    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
        # Convert the dataframe to an XlsxWriter Excel object
        df.to_excel(writer, sheet_name="Manufacturers", index=False)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets["Manufacturers"]

        # Add a format for the header
        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#D7E4BC",
                "border": 1,
            }
        )

        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Set the column width
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col))
            worksheet.set_column(i, i, column_len + 2)

    print(f"Excel file has been created: {output_excel}")
