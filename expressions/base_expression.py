from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Generator, Dict, Iterable, Tuple

from expressions.errors import InvalidExpressionError
from expressions.token import operators
from expressions.token import TokenType, Tokenizer, Token


_tokenizer = Tokenizer()


class ExpressionType(Enum):
    _BASE = auto()
    INFIX = auto()
    PREFIX = auto()
    POSTFIX = auto()


class BaseExpression(ABC):
    __type__ = ExpressionType._BASE

    def __init__(self, expression: str):
        self._tokens = self.tokenize(expression)
        self._vars = {}
        self._validate()

    def __str__(self):
        return ' '.join(str(t.value) for t in self._tokens)

    def variables_names(self) -> Tuple:
        names = set()
        for token in self._tokens:
            if token.type == TokenType.VARIABLE:
                names.add(token.value)
        return tuple(names)

    @property
    def variables(self):
        return self._vars

    def set_variables(self, **variables):
        self._vars = variables

    @classmethod
    def from_tokens(cls, tokens: Iterable[Token]):
        string = ' '.join(str(t.value) for t in tokens)
        # print(string)
        return cls(string)

    @property
    def value(self):
        return self._eval()

    @property
    def type(self):
        return self.__type__.name.lower()

    @property
    def tokens(self) -> List[Token]:
        return self._tokens

    @staticmethod
    def get_type(symbol: str):
        if len(symbol) != 1:
            raise ValueError('symbol must be a string of a length of 1')
        if symbol in operators:
            return TokenType.OPERATOR

    @staticmethod
    def tokenize(expression: str) -> List[Token]:
        global _tokenizer
        return _tokenizer.tokenize(expression)

    @abstractmethod
    def _eval(self) -> int:
        pass

    def _validate(self):
        prev_vars = self._vars
        self._vars = self._mock_variables()

        self._pre_validate()

        try:
            self._eval()
        except ZeroDivisionError:
            raise ZeroDivisionError('Expression contains division by zero')
        except Exception:
            raise InvalidExpressionError('Expression is invalid')
        finally:
            self._vars = prev_vars

    def _pre_validate(self) -> None:
        pass

    def _get_variable_value(self, token):
        var_name = token.value
        value = self._vars.get(var_name)
        if value is None:
            raise RuntimeError(f'Variable "{var_name}" is not defined')
        return value

    def _mock_variables(self, default_value: int = 1) -> Dict[str, int]:
        variables = {}
        for var in self.variables_names():
            variables[var] = default_value
        return variables
