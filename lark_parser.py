from zipfile import ZipFile
import xml.etree.ElementTree as ET

from lark import Lark, Transformer
import shutil
import openpyxl
import openpyxl.cell
import openpyxl.formula
import openpyxl.workbook
import openpyxl.worksheet
import openpyxl.worksheet.cell_range
import openpyxl.worksheet.formula


l = Lark.open("grammar.lark", start="formula")


class PythonTransformer(Transformer):
    def function(self, s):
        [excel_function, args] = s
        changed_names = {"AVERAGE": "mean"}
        python_name = changed_names.get(excel_function, excel_function.lower())
        match excel_function.type:
            case "SUFFIX_FUNCTION":
                return f"{args}.{python_name}()"
            case "PREFIX_FUNCTION":
                return f"{python_name}({args})"

    def calc(self, s):
        [left, operator, right] = s
        return f"{left}{operator}{right}"


class PythonInExcelTransformer(PythonTransformer):
    def RANGE(self, r):
        return f'xl("{r}")'

    def CELL_REF(self, r):
        return f'xl("{r}")'


def cell_to_ints(cell:str):
        col = cell[0]
        row = cell[1:]
        return ord(col) - 65, int(row) - 1

class PandasTransformer(PythonTransformer):
    def RANGE(self, r):
        [start,end]=r.split(":")
        col, row = cell_to_ints(start)
        col2, row2 = cell_to_ints(end)
        return f'df.iloc[{row}:{row2},{col}:{col2}]'

    def CELL_REF(self, r):
        col, row = cell_to_ints(r)
        return f'df.iat[{row},{col}]'
    

def transform_formula(formula, transformer):
    tree = l.parse(formula)
    python_formula = transformer().transform(tree)
    return python_formula


original_file = "../test.xlsx"
original_excel = openpyxl.load_workbook(original_file)
sheet = original_excel.active
for value in sheet.iter_rows():
    for cell in value:
        if cell.data_type == "f":
            formula = cell.value
            if not isinstance(formula, openpyxl.worksheet.formula.ArrayFormula):
                python_formula = transform_formula(formula, PythonInExcelTransformer)
                # cell.value = "_xlfn._xlws.PY(1,1,C4,C4)"
                sheet[cell.coordinate] = openpyxl.worksheet.formula.ArrayFormula(
                    cell.coordinate, python_formula
                )
                print(python_formula)
# original_excel.save('python.xlsx')
