import math

def to_rpn(expression_list):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
    functions = {"sqrt", "root", "sin", "cos", "tan", "asin", "acos", "atan"}
    
    output = []
    operators = []

    for i, token in enumerate(expression_list):
        token = token.lower()
        if token.isdigit() or "." in token:
            output.append(token)
        elif token in functions:
            operators.append(token)   
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()

            if operators and operators[-1] in functions:
                output.append(operators.pop())
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        else:
            if output and output[-1].isdigit():
                output.append("*")
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output

def calculate_rpn(rpn_list):
    stack = []

    for token in rpn_list:
        if token.replace(".", "").isdigit():
            stack.append(float(token))
        elif token in {"+", "-", "*", "/", "%", "^"}:
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "%":
                stack.append(a % b)
            elif token == "^":
                stack.append(a ** b)
        elif token == "root":
            b = stack.pop()
            a = stack.pop()
            stack.append(a ** (1 / b))
        elif token in {"sqrt", "sin", "cos", "tan", "asin", "acos", "atan"}:
            a = stack.pop()

            if token == "sqrt":
                stack.append(math.sqrt(a))
            elif token == "sin":
                stack.append(math.sin(math.radians(a)))
            elif token == "cos":
                stack.append(math.cos(math.radians(a)))
            elif token == "tan":
                stack.append(math.tan(math.radians(a)))
            elif token == "asin":
                stack.append(math.asin(math.radians(a)))
            elif token == "acos":
                stack.append(math.acos(math.radians(a)))
            elif token == "atan":
                stack.append(math.atan(math.radians(a)))

    return stack[0] if stack else None

def get_valid_expression():
    while True:
        expression_input = input("Enter expression: ")
        expression_list = []
        current_chunk = ""
        valid_chars = set("0123456789+-*/%^().sqrtrootasinacosatan")

        for char in expression_input:
            if char.lower() in valid_chars:
                current_chunk += char.lower()
            elif char.strip():
                if current_chunk:
                    expression_list.append(current_chunk)
                    current_chunk = ""
                expression_list.append(char.lower())

        if current_chunk:
            expression_list.append(current_chunk)

        if expression_list and expression_list[0] not in "+-*/%^" and expression_list[-1] not in "+-*/%^":
            return expression_list
        else:
            print("Invalid input. Please enter a valid mathematical expression.")

def main():
    expression_list = get_valid_expression()
    rpn_result = to_rpn(expression_list)
    try:
        result = calculate_rpn(rpn_result)
        if result is not None:
            if float(result) == int(result):
                print("Result:", int(result))
            else:
                print("Result:", result)
        else:
            print("Error: Could not calculate the result.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
