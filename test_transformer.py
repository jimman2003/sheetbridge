from lark import Lark
import pytest
from lark_parser import transform_formula


l = Lark.open("grammar.lark")


@pytest.mark.parametrize(
    "formula,python_formula",
    [
        ("=SUM(A1:A2)", 'xl("A1:A2").sum()'),
        ("=SUM(B1:B2)", 'xl("B1:B2").sum()'),
        ("=SUM(A3:B3)", 'xl("A3:B3").sum()'),
        ("=AVERAGE(A1:A2)", 'xl("A1:A2").mean()'),
        ("=AVERAGE(B1:B2)", 'xl("B1:B2").mean()'),
    ],
)
def test_suffix(formula: str, python_formula: str):
    assert transform_formula(formula) == python_formula
