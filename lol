def scan(code):
    #print(code)
    #code = code.strip() + " "
    reserved_tokens = {'if', 'then', 'else', 'end', 'repeat', 'until', 'read', 'write'}
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
    state = 'start'
    token = ""
    i = 0
    code_length = len(code)
    line = 1
    passed = False
    while i < code_length:
        char = code[i]

        if state == 'start':
            if char == '\n':
                if code [i-1] == ';' and passed:
                    return ["syntax error : in line " + str(line) + ", unexpected token"]
                if code[i-1] == ';' or code[i-1] == '}' or passed:
                    line +=1
                    passed = False
                else:
                    return ["syntax error : in line " + str(line) + ", unexpected token"]

            elif char == '\n':
                line +=1

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
                    return ["syntax error : in line " + str(line) + ", unexpected token"]

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
                return ["syntax error : in line " + str(line) + ", unexpected token"]

            state = 'start'
            i += 1

    tokens_list = []
    for x, y in zip(tokens, tokens_type):
        #if y != 'Unknown':
            #print(x, ",", y)
        tokens_list.append({x, y})
            #tokens_list.append({"token_value": x, "token_type": y})

    return tokens_list


codee = """
{S}
read x; {input an integer}
if 0 < x then  {don't compute if x <= 0}
    fact := 1;
    repeat
        fact := fact * x;
    until x := 0;
    write fact {output factorial of x}
end
"""
#scan(codee.strip())
#fun(codee)



codeee = []
while True:
    user_input = input()
    if user_input == '':
        break
    else:
        codeee.append(user_input+'\n')


print(scan(''.join(codeee)))

#print(scan(codee.strip()))


"""
{Sample program in TINY language - computes factorial}
read x; {input an integer}
if 0 < x then  {don't compute if x <= 0}
    fact := 1;
    repeat
        fact := fact * x;
    until x := 0;
    write fact {output factorial of x}
end
"""
