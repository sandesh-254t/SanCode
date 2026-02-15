import sys

variables = {}

# -------------------------
# AUTO TYPE DETECTION
# -------------------------
def auto_detect(value):

    # Remove surrounding single quotes if present
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    # Try integer
    try:
        if "." in value:
            return float(value)
        return int(value)
    except:
        return value  # treat as string


def get_value(token):

    # String literal in code
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]

    # Number detection
    try:
        if "." in token:
            return float(token)
        return int(token)
    except:
        pass

    # Variable lookup
    if token in variables:
        return variables[token]

    raise Exception(f"Undefined variable: {token}")


# -------------------------
# EXPRESSION EVALUATION
# -------------------------
def evaluate(words):

    # NOT operator
    if words[0] == "not":
        return not evaluate(words[1:])

    # Logical AND
    if "and" in words:
        index = words.index("and")
        return evaluate(words[:index]) and evaluate(words[index+1:])

    # Logical OR
    if "or" in words:
        index = words.index("or")
        return evaluate(words[:index]) or evaluate(words[index+1:])

    # Single value
    if len(words) == 1:
        return get_value(words[0])

    # Binary operations only (architecture limit)
    left = get_value(words[0])
    op = words[1]
    right = get_value(words[2])

    if op == "add":
        return left + right
    if op == "sub":
        return left - right
    if op == "mul":
        return left * right
    if op == "div":
        if right == 0:
            raise Exception("Division by zero")
        return left / right

    if op == "greater":
        return left > right
    if op == "less":
        return left < right
    if op == "equal":
        return left == right
    if op == "notequal":
        return left != right
    if op == "greaterequal":
        return left >= right
    if op == "lessequal":
        return left <= right

    raise Exception("Invalid expression")


# -------------------------
# MAIN EXECUTION
# -------------------------
def run_line(line):

    line = line.strip()

    if not line or line.startswith("#"):
        return

    # -------------------------
    # INPUT
    # -------------------------
    if line.startswith("ask"):

        parts = line.split(" as ")

        if len(parts) != 2:
            raise Exception("Invalid ask syntax")

        left = parts[0].split()
        if len(left) != 2:
            raise Exception("Invalid ask variable")

        var = left[1]
        prompt = parts[1].strip()

        if not (prompt.startswith("'") and prompt.endswith("'")):
            raise Exception("Prompt must be in single quotes")

        prompt_text = prompt[1:-1]

        user_input = input(prompt_text)
        variables[var] = auto_detect(user_input)

        return

    # -------------------------
    # FOR LOOP
    # -------------------------
    if line.startswith("repeat") and "times," in line:

        header, action = line.split("times,", 1)
        parts = header.split()

        if len(parts) != 4:
            raise Exception("Invalid repeat syntax")

        _, var, count = parts[0], parts[1], parts[2]

        count_value = get_value(count)

        if not isinstance(count_value, int):
            raise Exception("Repeat count must be integer")

        for i in range(count_value):
            variables[var] = i
            run_line(action.strip())

        return

    words = line.split()

    # -------------------------
    # WHEN / OTHERWISE
    # -------------------------
    if words[0] == "when" or words[0] == "otherwise":

        i = 0

        while i < len(words):

            if words[i] == "when":

                condition = evaluate(words[i+1:i+4])

                j = i + 4
                while j < len(words) and words[j] != "otherwise":
                    j += 1

                action = words[i+4:j]

                if condition:
                    run_line(" ".join(action))
                    return

                i = j

            elif words[i] == "otherwise":

                if i + 1 < len(words) and words[i+1] == "when":
                    i += 1
                else:
                    action = words[i+1:]
                    run_line(" ".join(action))
                    return

            else:
                i += 1

        return

    # -------------------------
    # OUTPUT
    # -------------------------
    if words[0] == "say":
        result = evaluate(words[1:])

        if isinstance(result, float) and result.is_integer():
            print(int(result))
        else:
            print(result)
        return

    # -------------------------
    # VARIABLE ASSIGNMENT
    # -------------------------
    variables[words[0]] = evaluate(words[1:])


# -------------------------
# FILE RUNNER
# -------------------------
def run_file(filename):
    with open(filename, "r") as f:
        for line in f:
            run_line(line)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        print("Usage: python lan.py program.sc")
