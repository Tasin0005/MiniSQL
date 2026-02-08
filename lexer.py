
class Token:
    def __init__(self, category, value):
        self.category = category # tokens can either be: keywords, identifiers, separators, operators, numbers, strings
        self.value = value # the actual value of the token

def lex(input_string):
    token_stream = []
    index = 0
    while index < len(input_string):
        if (input_string[index] == ' '):
            index += 1
            continue
        elif is_keyword(input_string, index):
            keyword, ending_index = get_keyword(input_string, index) # ending_index should be the index of space after the token, if the token is at the end of the string, it should be len(input_string)
            token_stream.append(Token("keyword", keyword))
            index = ending_index
        elif is_string(input_string, index):
            string, ending_index = get_string(input_string, index)
            token_stream.append(Token("string", string))
            index = ending_index
        elif is_separator(input_string, index):
            separator, ending_index = get_separator(input_string, index)
            token_stream.append(Token("separator", separator))
            index = ending_index
        elif is_operator(input_string, index):
            operator, ending_index = get_operator(input_string, index)
            token_stream.append(Token("operator", operator))
            index = ending_index
        elif is_number(input_string, index):
            number, ending_index = get_number(input_string, index)
            token_stream.append(Token("number", number))
            index = ending_index
        elif is_identifier(input_string, index):
            identifier, ending_index = get_identifier(input_string, index)
            token_stream.append(Token("identifier", identifier))
            index = ending_index
        else:
            print("Please enter a valid SQL command")
            break

    return token_stream

def is_keyword(input_string, index):
    keywords = ["CREATE", "TABLE", "INSERT", "INTO", "VALUES", "SELECT", "FROM", "WHERE", "UPDATE", "SET", "DELETE", "DROP", "*"]
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index] != ' ':
        ending_index += 1
    word = input_string[index:ending_index].upper()
    for keyword in keywords:
        if word == keyword:
            return True
    return False

def get_keyword(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index] != ' ':
        ending_index += 1
    keyword = input_string[index:ending_index].upper()
    return keyword, ending_index

def is_string(input_string, index):
    if input_string[index] == '"':
        ending_index = index + 1
        while ending_index < len(input_string) and input_string[ending_index] != '"':
            ending_index += 1
        if (ending_index < len(input_string)):
            return True
    else:
        return False

def get_string(input_string, index):
    ending_index = index + 1
    while ending_index < len(input_string) and input_string[ending_index] != '"':
        ending_index += 1
    string = input_string[index:ending_index + 1]
    return string, ending_index + 1

def is_separator(input_string, index):
    separators = [',', '(', ')', ';']
    for i in range(len(separators)):
        if input_string[index] == separators[i]:
            return True
    return False

def get_separator(input_string, index):
    return input_string[index], index + 1

def is_operator(input_string, index):
    operators = ['>=', '<=', '!=', '=', '>', '<', '+', '-']
    for operator in operators:
        if input_string[index:].startswith(operator):
            return True
    return False

def get_operator(input_string, index):
    operators = ['>=', '<=', '!=', '=', '>', '<', '+', '-']
    for operator in operators:
        if input_string[index:].startswith(operator):
            return operator, index + len(operator)

def is_number(input_string, index):
    if not input_string[index].isdigit():
        return False
    
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index].isdigit():
        ending_index += 1

    # check if number is followed by a letter/underscore (meaning its treated as an identifier)
    if ending_index < len(input_string) and (input_string[ending_index].isalpha() or input_string[ending_index] == '_'):
        return False
    return True

def get_number(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and input_string[ending_index].isdigit():
        ending_index += 1
    number = input_string[index:ending_index]
    return number, ending_index

def is_identifier(input_string, index):
    if input_string[index].isalnum() or input_string[index] == '_':
        return True
    return False

def get_identifier(input_string, index):
    ending_index = index
    while ending_index < len(input_string) and (input_string[ending_index].isalnum() or input_string[ending_index] == '_'):
        ending_index += 1
    identifier = input_string[index:ending_index]
    return identifier, ending_index