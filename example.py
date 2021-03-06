from math import e, cos, log, sin, pi  # noqa
from typing import Type

from expressions.base_expression import BaseExpression
from expressions import InfixExpression, to_postfix, to_prefix, to_infix, PostfixExpression


def evaluable(exp: str, variables: dict):
    result = exp
    for k, v in variables.items():
        result = result.replace(k, str(v))
    result = result.replace('^', '**').replace('ln', 'log')
    return result


def check_expression(expression: str, variables: dict, python_eval: bool = False, type_: Type[BaseExpression] = InfixExpression):
    print(f'Testing expression: {expression}')
    print('-' * 120)

    if python_eval:
        try:
            eval_ = eval(evaluable(expression, variables))
        except Exception as e:
            eval_ = f'raised {e.__class__.__name__}: {e}'
        print(f'Python built-in eval: {eval_}')

    tokens = BaseExpression.tokenize(expression)
    print(f'tokenizer result: {tokens}')
    print(f'tokenizer result (tokens values): ', end='')
    for token in tokens:
        print(token, end=' ')
    print()
    s = type_(expression)
    s.set_variables(**variables)
    print(f'Expression value: {s.value}')
    print()


def main():
    infix_expressions = {
        1: ('1+ 2*e^x - (10 * 2 ^ cos(4*x)  -ln(4)*abs(log2(sin(522.44-pi*2))))', {'x': 10}),
        2: ('1  + 2*e^x - (10 * 2 ^ (4*x)  -4*522.44-pi*2)', {'x': 10}),
        100: ('1 + 2 * 2 ^ 10 - ( 10 * 2 ^ ( 4 * 10 ) - 4 * 522.44 - 3 * 2 )', {}),
        3: ('lg(14+2)', {}),
        4: ('+4 - (-1)', {}),
        5: ('+-+4 +(- (---1))', {}),
        6: ('----+--(-++-++-(-1))', {}),
        7: ('((-(((-(-1))))))', {}),
        8: ('(1)', {}),
        9: ('abs(-16)', {}),
        10: ('1-A%4', {'A': 8}),
        11: ('(-1 // 0.4)', {})
    }

    # check_expression(*infix_expressions[11], python_eval=True)

    prefix_expressions = {
        1: ('+ 2 * e / 2 x', {'x': e}),
        2: ('// + abs A e 9.4', {'x': -16}),
        3: ('- 4', {}),
    }

    # check_expression(*prefix_expressions[3], type_=PrefixExpression)

    postfix_expressions = {
        1: ('', {'x': e}),
        2: ('x abs 2 + 9.4 //', {'x': -16}),
        3: ('4 -', {}),
        4: ('8 / 3 pi * 2 -', {'z': 8})
    }

    # check_expression(*postfix_expressions[4], type_=PostfixExpression)
    # 12 4 2 3 5 1 - + * + - abs fact
    check_expression('12 4 2 3 5 1 - + * + - abs fact', {}, type_=PostfixExpression)

    case = 100
    infix = InfixExpression(infix_expressions[case][0])
    infix.set_variables(**infix_expressions[case][1])
    print(f'Input: {infix} = {infix.value}')
    postfix = to_postfix(infix)
    print(f'Postfix: {postfix} = {postfix.value}')
    prefix = to_prefix(postfix)
    print(f'Prefix {prefix} = {prefix.value}')
    infix = to_infix(prefix)
    print(f'Infix: {infix} = {infix.value}')


if __name__ == '__main__':
    main()
