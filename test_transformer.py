from lark import Lark
import pytest
from lark_parser import transform_formula


l = Lark.open("grammar.lark")


@pytest.mark.parametrize(
    "formula,python_formula",
    [
        ("=SUM(A1:A2)", 'xl("A1:A2").sum()'),
        ("=AVERAGE(B1:B2)", 'xl("B1:B2").mean()'),
    ],
)
def test_suffix_functions(formula: str, python_formula: str):
    assert transform_formula(formula) == python_formula

@pytest.mark.parametrize(
    "formula,python_formula",
    [
        ("=A1*A2", 'xl("A1")*xl("A2")'),
        ("=A1+A2+A3", 'xl("A1")+xl("A2")+xl("A3")'),
    ]
)
def test_infix_operators(formula: str, python_formula: str):
    assert transform_formula(formula) == python_formula
