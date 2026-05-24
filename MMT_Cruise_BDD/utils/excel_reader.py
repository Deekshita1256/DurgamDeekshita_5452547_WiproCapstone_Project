import openpyxl
import os

class ExcelReader:
    @staticmethod
    def read_excel(file_name, sheet_name):
        """
        Reads data from an Excel file located inside the 'data' folder 
        and converts rows into a dictionary list format.
        """
        # Strategy A: Look for the file inside your project's data folder relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_a = os.path.abspath(os.path.join(current_dir, '..', 'data', file_name))
        
        # Strategy B: Fallback assuming execution starts from project root
        path_b = os.path.abspath(os.path.join(os.getcwd(), 'data', file_name))
        
        # Path selection guard
        if os.path.exists(path_a):
            target_path = path_a
        elif os.path.exists(path_b):
            target_path = path_b
        else:
            raise FileNotFoundError(
                f"\n❌ CRITICAL EXCEL CONFIGURATION FAILURE:\n"
                f"The Excel data file '{file_name}' was not found inside your 'data' folder!\n"
                f"We scanned the following absolute locations:\n"
                f" 1. {path_a}\n"
                f" 2. {path_b}\n"
                f"Please make sure the folder is named exactly 'data' and your file is inside it."
            )

        workbook = openpyxl.load_workbook(target_path)
        sheet = workbook[sheet_name]
        
        # Logic to parse the spreadsheet rows into usable key-value pairs
        data_list = []
        header = [cell.value for cell in sheet[1]]
        
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if any(row):  # Skip completely empty rows
                data_list.append(dict(zip(header, row)))
                
        return data_list