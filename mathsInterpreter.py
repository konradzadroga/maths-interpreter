import regex
import shlex

class Checker:
    @staticmethod
    def is_number(token):
        number_pattern = r'[0-9a-z]+'
        matches_number = regex.match(number_pattern, token)
        if matches_number:
            return True
        else:
            return False

    @staticmethod
    def is_variable(token):
        variable_pattern = r'[a-z]+$'
        matches_variable = regex.match(variable_pattern, token)
        if matches_variable:
            return True
        else:
            return False

    @staticmethod
    def is_operator(token):
        operator_pattern = r'[\+\-\*\=]'
        matches_operator = regex.match(operator_pattern, token)
        if matches_operator:
            return True
        else:
            return False

    @staticmethod
    def is_left_bracket(token):
        left_bracket_pattern = r'\('
        matches_left_bracket = regex.match(left_bracket_pattern, token)
        if matches_left_bracket:
            return True
        else:
            return False

    @staticmethod
    def is_right_bracket(token):
        right_bracket_pattern = r'\)'
        matches_right_bracket = regex.match(right_bracket_pattern, token)
        if matches_right_bracket:
            return True
        else:
            return False

    @staticmethod
    def is_var_in_dictionary(var, dictionary):
        if var in dictionary:
            return True
        else:
            return False

    @staticmethod
    def is_expression_an_assignment(expression):
        assignment_pattern = r'([a-z]+)=([^=])*'
        matches_assignment = regex.match(assignment_pattern, expression)
        if matches_assignment:
            return matches_assignment

    @staticmethod
    def does_it_contains_illegal_characters(expression):
        illegal_pattern = r'.*[!@$%&~`].*'
        matches_illegal = regex.match(illegal_pattern,expression)
        if matches_illegal:
            return True
        return False

class Converter:
    @staticmethod
    def convert_to_rpn(tokens):
        output = []
        operator_stack = []
        if tokens!=None:
            for i in range(len(tokens)):
                if Checker.is_number(tokens[i]):
                    output.append(tokens[i])
                elif Checker.is_operator(tokens[i]):
                    if len(operator_stack) != 0:
                        if (tokens[i] == '+' or tokens[i] == '-'):
                            while ((operator_stack[0] == '*') or (
                                    operator_stack[0] == '+' or operator_stack[0] == '-')) and (operator_stack[0] != '('):
                                output.append(operator_stack.pop(0))
                                if len(operator_stack) == 0:
                                    break
                        elif (tokens[i] == '*'):
                            while (operator_stack[0] == '*' or operator_stack[0] == '/')  and (operator_stack[0] != '('):
                                output.append(operator_stack.pop(0))
                                if len(operator_stack) == 0:
                                    break
                    operator_stack.insert(0, tokens[i])
                elif Checker.is_left_bracket(tokens[i]):
                    operator_stack.insert(0, tokens[i])
                elif Checker.is_right_bracket(tokens[i]):
                    if len(operator_stack) != 0:
                        while (operator_stack[0] != '('):
                            output.append(operator_stack.pop(0))
                        operator_stack.pop(0)
            while (len(operator_stack) != 0):
                output.append(operator_stack.pop(0))
            return output
        else:
            return None

    @staticmethod
    def vars_to_numbers(list, dictionary):
        count_vars = 0
        count_vars_in_dict = 0
        for i in range(len(list)):
            if Checker.is_variable(list[i]):
                count_vars += 1
                if list[i] in dictionary:
                    list[i] = str(dictionary[list[i]])
                    count_vars_in_dict += 1
        if count_vars == count_vars_in_dict:
            return list

    @staticmethod
    def convert_from_infix_to_calculated(expression,dictionary):
        tokens = list(shlex.shlex(expression))
        converted = Converter.vars_to_numbers(tokens, dictionary)
        converted = Converter.convert_to_rpn(converted)
        if Interpreter.check_expression_validity(tokens, converted,expression):
            out = Calculator.calculate(converted)
            return out

    @staticmethod
    def remove_spaces(string):
        m = regex.match('.*', string)
        if m:
            string = regex.sub(r'\s*', '', string)
        return string

    @staticmethod
    def make_string_valid(string):
        m = regex.findall('.*', string)
        if m:
            string = regex.sub(r'[=]-','=0-',string)
            string = regex.sub(r'[^0-9a-z(]-|^-', '0-', string)
            string = regex.sub(r'[(]-|^-', '(0-', string)
        return string

class Calculator:
    @staticmethod
    def calculate(tokens):
        stack = []
        for i in range(len(tokens)):
            if Checker.is_number(tokens[i]):
                stack.insert(0, int(tokens[i]))
            elif Checker.is_operator(tokens[i]):
                a = stack.pop(0)
                if len(stack) != 0:
                    b = stack.pop(0)
                    if tokens[i] == '+':
                        stack.insert(0, (lambda a, b: a + b)(b, a))
                    elif tokens[i] == '-':
                        stack.insert(0, (lambda a, b: a - b)(b, a))
                    elif tokens[i] == '*':
                        stack.insert(0, (lambda a, b: a * b)(b, a))

        output = stack.pop(0)
        return output

class Interpreter:

    dictionary = {}

    @staticmethod
    def what_expression_it_is(expression):
        if Checker.is_variable(expression):
            return 1
        if Checker.is_expression_an_assignment(expression) != None:
            return 2
        else:
            return 3

    @staticmethod
    def check_expression_validity(tokens, list, expression):
        if Checker.does_it_contains_illegal_characters(expression):
            return False
        if list == None:
            return False
        if Checker.is_operator(tokens[len(tokens) - 1]):
            return False

        return True

    def do_the_job_with_expression(self, expression):

        if self.what_expression_it_is(expression) == 1:
            if (Checker.is_var_in_dictionary(expression, self.dictionary)):
                print(self.dictionary[expression])
            else:
                print('????????')
        elif self.what_expression_it_is(expression) == 2:
            exp = ''
            for i in range(len(Checker.is_expression_an_assignment(expression).captures(2))):
                exp += Checker.is_expression_an_assignment(expression).captures(2)[i]
            if Converter.convert_from_infix_to_calculated(exp,self.dictionary) != None:
                self.dictionary[Checker.is_expression_an_assignment(expression).group(1)] = Converter.convert_from_infix_to_calculated(exp,self.dictionary)
            else:
                print('ERROR')

        elif self.what_expression_it_is(expression) == 3:
            if Converter.convert_from_infix_to_calculated(expression,self.dictionary) != None:
                print(Converter.convert_from_infix_to_calculated(expression,self.dictionary))
            else:
                print('ERROR')

    @staticmethod
    def start_the_interpreter():
        #print('Welcome to maths interpreter. You can perform math operations there. You can add, sub and multiply digits and variables.')
        while True:
            try:
                string = input("Write here: ")
                string = Converter.remove_spaces(string)
                string = Converter.make_string_valid(string)
                interpreter.do_the_job_with_expression(string)
            except(EOFError):
                print("End of file")
                break

interpreter = Interpreter()
interpreter.start_the_interpreter();