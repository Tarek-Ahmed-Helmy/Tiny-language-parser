def scan(code):
    reserved_tokens = {'if', 'then', 'end', 'repeat', 'until', 'read', 'write'}
    special_chars = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULT',
        '/': 'DIV',
        '=': 'EQUAL',
        '<': 'LESSTHAN',
        '(': 'OPENBRACKET',
        ')': 'CLOSEDBRACKET',
        ';': 'SEMICOLON',
        ':=': 'ASSIGN'
    }
    tokens, tokens_type = [], []
    i = 0
    codeLine = 1
    state = 'start'
    token = ""
    code_length = len(code)
    passed = False
    while i < code_length:
        char = code[i]
        if state == 'start':
            if char == '\n':
                if code[i - 1] == ';' and passed:
                    return ["syntax error : in line " + str(codeLine) + ", unexpected token"], False

                if code[i - 1] == ';' or code[i - 1] == '}' or passed:
                    codeLine += 1
                    passed = False

                else:
                    return ["syntax error : in line " + str(codeLine) + ", unexpected token"], False

            elif char == '\n':
                codeLine += 1

            elif char == '{':
                state = 'in_comment'

            elif char.isdigit():
                token += char
                state = 'in_number'

            elif char.isalpha():
                token += char
                state = 'in_identifier'

            elif char == ':':
                state = 'in_assign'

            elif char != ' ' and char != '\n' and char != '\t':
                tokens.append(char)
                if char in special_chars:
                    tokens_type.append(special_chars[char])
                else:
                    return ["syntax error : in line " + str(codeLine) + ", unexpected token"], False
            i += 1

        elif state == 'in_comment':
            if char == '}':
                state = 'start'
            i += 1

        elif state == 'in_identifier':
            if char.isalpha():
                token += char
                i += 1
            else:
                tokens.append(token)
                if token in reserved_tokens:
                    tokens_type.append(token.upper())
                    if token == 'repeat' or token == 'then' or token == 'end':
                        passed = True
                else:
                    tokens_type.append('IDENTIFIER')
                token = ''
                state = 'start'

        elif state == 'in_number':
            if char.isdigit():
                token += char
                i += 1
            else:
                tokens.append(token)
                tokens_type.append('NUMBER')
                token = ''
                state = 'start'

        else:
            if char == '=':
                tokens.append(':=')
                tokens_type.append('ASSIGN')
            else:
                return ["syntax error : in line " + str(codeLine) + ", unexpected token"], False
            state = 'start'
            i += 1

    tokens_list = []
    for x, y in zip(tokens, tokens_type):
        print(x, ",", y)
        tokens_list.append([x, y])
    return tokens_list, True


sourceCode = []
while True:
    user_input = input()
    if user_input == '':
        break
    else:
        sourceCode.append(user_input + '\n')

result = scan(''.join(sourceCode))
outputTokens = open("Tokens.txt", "w")
outputTokens.write('')
outputTokens = open("Tokens.txt", "a")
if result[1]:
    for line in result[0]:
        comma = True
        for element in line:
            outputTokens.write(str(element))
            if comma:
                outputTokens.write(' , ')
                comma = False
        outputTokens.write('\n')
else:
    print(''.join(result[0]))
    outputTokens.write(''.join(result[0]))

outputTokens.close()
