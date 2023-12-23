def scan(code):
    code = code.strip() + " "
    reserved_tokens = {'if', 'else', 'then', 'end', 'repeat', 'until', 'read', 'write'}
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
    state = 'start'
    token = ""
    code_length = len(code)
    while i < code_length:
        char = code[i]
        if state == 'start':
            if char == '{':
                state = 'in_comment'

            elif char.isdigit():
                token += char
                state = 'in_number'

            elif char.isalpha():
                token += char
                state = 'in_identifier'

            elif char == ':':
                state = 'in_assign'

            elif char != ' ' and char != '\n':
                tokens.append(char)
                if char in special_chars:
                    tokens_type.append(special_chars[char])
                else:
                    tokens_type.append("syntax error")
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
                tokens.append(':')
                tokens_type.append('syntax error')
            state = 'start'
            i += 1

    tokens_list = []
    for x, y in zip(tokens, tokens_type):
        if y != 'syntax error':
            tokens_list.append([x, y])

    return tokens_list
