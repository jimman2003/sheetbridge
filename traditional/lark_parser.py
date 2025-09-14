from lark import Lark, Transformer

l = Lark.open("grammar.lark", start="formula")


class PythonTransformer(Transformer):
    def function(self, s):
        [excel_function, args] = s
        changed_names = {"AVERAGE": "mean", "UNIQUE": "pd.unique"}
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


def cell_to_ints(cell: str):
    col = cell[0]
    row = cell[1:]
    return ord(col) - 65, int(row) - 1


class PandasTransformer(PythonTransformer):
    def RANGE(self, r):
        [start, end] = r.split(":")
        col, row = cell_to_ints(start)
        col2, row2 = cell_to_ints(end)
        row_expr = f"{row}:{row2}" if row != row2 else f"{row}"
        col_expr = f"{col}:{col2}" if col != col2 else f"{col}"
        return f"df.iloc[{row_expr},{col_expr}]"

    def CELL_REF(self, r):
        col, row = cell_to_ints(r)
        return f"df.iat[{row},{col}]"


def transform_formula(formula, transformer):
    tree = l.parse(formula)
    python_formula = transformer().transform(tree)
    return python_formula
