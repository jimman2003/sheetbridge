import time
import logging
import openpyxl
from traditional.lark_parser import transform_formula

# Configure logging for timing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def time_function(func_name: str):
    """Decorator to time function execution and log results."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                logger.info(f"{func_name} executed in {execution_time:.3f} seconds")
                return result
            except Exception as e:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.error(f"{func_name} failed after {execution_time:.3f} seconds: {str(e)}")
                raise
        return wrapper
    return decorator


@time_function("Transform Excel Sheet")
def transform_excel_sheet(sheet, transformer):
    for value in sheet.iter_rows():
        for cell in value:
            if cell.data_type == "f":
                formula = cell.value
                if not isinstance(formula, openpyxl.worksheet.formula.ArrayFormula):
                    yield transform_formula(formula, transformer)


@time_function("Transform Excel File")
def transform_excel(file, transformer):
    original_excel = openpyxl.load_workbook(file)
    sheet = original_excel.active
    return list(transform_excel_sheet(sheet, transformer))
