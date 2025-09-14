import openpyxl
from traditional.lark_parser import transform_formula


def transform_excel_sheet(sheet, transformer):
    for value in sheet.iter_rows():
        for cell in value:
            if cell.data_type == "f":
                formula = cell.value
                if not isinstance(formula, openpyxl.worksheet.formula.ArrayFormula):
                    yield transform_formula(formula, transformer)


def transform_excel(file, transformer):
    original_excel = openpyxl.load_workbook(file)
    sheet = original_excel.active
    return list(transform_excel_sheet(sheet, transformer))
