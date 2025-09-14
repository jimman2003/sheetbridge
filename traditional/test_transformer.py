import pytest
from lark_parser import transform_formula, PythonInExcelTransformer, PandasTransformer


@pytest.mark.parametrize(
    "formula,expected,transformer",
    [
        ("=SUM(A1:A2)", 'xl("A1:A2").sum()', PythonInExcelTransformer),
        ("=AVERAGE(B1:B2)", 'xl("B1:B2").mean()', PythonInExcelTransformer),
        ("=SUM(A1:A2)", "df.iloc[0:1,0].sum()", PandasTransformer),
        ("=AVERAGE(B1:B2)", "df.iloc[0:1,1].mean()", PandasTransformer),
    ],
)
def test_suffix_functions(formula: str, expected: str, transformer):
    assert transform_formula(formula, transformer) == expected


@pytest.mark.parametrize(
    "formula,expected,transformer",
    [
        ("=A1*A2", 'xl("A1")*xl("A2")', PythonInExcelTransformer),
        ("=A1+A2+A3", 'xl("A1")+xl("A2")+xl("A3")', PythonInExcelTransformer),
        ("=2*A1", '2*xl("A1")', PythonInExcelTransformer),
        ("=A1*A2", "df.iat[0,0]*df.iat[1,0]", PandasTransformer),
        ("=A1+A2+A3", "df.iat[0,0]+df.iat[1,0]+df.iat[2,0]", PandasTransformer),
        ("=2*A1", "2*df.iat[0,0]", PandasTransformer),
    ],
)
def test_infix_operators(formula: str, expected: str, transformer):
    assert transform_formula(formula, transformer) == expected


@pytest.mark.parametrize(
    "formula,expected,transformer",
    [
        ("=UNIQUE(A1:A10)", "pd.unique(df.iloc[0:9,0])", PandasTransformer),
    ],
)
def test_prefix_functions(formula: str, expected: str, transformer):
    assert transform_formula(formula, transformer) == expected
