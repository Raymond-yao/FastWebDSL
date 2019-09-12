from .Token import *
from enum import Enum


class State(int, Enum):
    # handle brackets, EOF, \n, Spaces(\t, \r, \s), Equal(=) and Comma(,)
    GENERAL = 1
    # handle function name (e.g. Nav, Link ...) and Variable names (new_nav = ....)
    IDENTIFIER = 2
    STRING = 3       # handle strings ... (e.g. "abc")
    NUMBER = 4       # handle number ... (e.g. 123)


class Tokenizer:

    """
        1) Tokenizer works as a state machine: we can almost immediately know the next state given the read character.
        2) The initial state starts from GENERAL.
        3) Cases for strings and numbers require caching the previous characters will be stored in char_buffer,
            the buffer gets cleared by the handler when handlers detect the sequence is complete
        4) The final built token result will be in list_of_tokens
    """

    spacing_characters = {" ", "\t", "\r"}
    brackets = {"(", ")", "{", "}"}

    def __init__(self):
        self.current_state = State.GENERAL
        self.char_buffer = []
        self.list_of_tokens = []

    def read_file(self, path):
        """
            read_file(string) -> [Token]
            Consumes a file and returns a list of corresponding tokens
        """
        with open(path, "r") as file:
            self.current_state = State.GENERAL
            self.char_buffer.clear()
            self.list_of_tokens.clear()

            for line in file:
                for char_read in line:
                    self.state_handler(char_read)

        # the char_buffer might still contain things when we reach the end of the input string
        if len(self.char_buffer) != 0:
            # a hack here, we pretend the last character seen as a None object
            self.state_handler(None)

        if self.current_state != State.GENERAL:
            # the input code is not valid
            raise Exception()
        else:
            return self.list_of_tokens

    def read(self, input_string):
        """
            read(string) -> [Token]
            Consumes an input program string and returns a list of corresponding tokens
        """
        self.current_state = State.GENERAL
        self.char_buffer.clear()
        self.list_of_tokens.clear()

        for char_read in input_string:
            self.state_handler(char_read)

        # the char_buffer might still contain things when we reach the end of the input string
        if len(self.char_buffer) != 0:
            # a hack here, we pretend the last character seen as a None object
            self.state_handler(None)

        if self.current_state != State.GENERAL:
            # the input code is not valid
            raise Exception()
        else:
            return self.list_of_tokens

    def state_handler(self, ch):  # no switch statement in py, python sucks!
        """
            state_handler(character) -> Void
            according to the current state, choose the correct state_handler
            and might add some tokens to the final result.
        """
        if self.current_state == State.GENERAL:
            self.handle_general(ch)
        elif self.current_state == State.STRING:
            self.handle_string(ch)
        elif self.current_state == State.NUMBER:
            self.handle_number(ch)
        elif self.current_state == State.IDENTIFIER:
            self.handle_identifier(ch)
        else:
            raise Exception("Invalid state")

    def handle_general(self, char):
        if char == None or char in self.spacing_characters:
            return
        elif char in self.brackets:
            self.add_token(Bracket(char))
        elif char == "\n":
            self.add_token(NewLine())
        elif char == "=":
            self.add_token(Eq())
        elif char == ",":
            self.add_token(Comma())
        else:
            self.char_buffer.clear()
            if char == "\"":
                self.current_state = State.STRING
            elif char.isdigit():
                self.char_buffer.append(char)
                self.current_state = State.NUMBER
            elif char.isalpha():
                self.char_buffer.append(char)
                self.current_state = State.IDENTIFIER
            else:
                raise InvalidTokenError("Invalid character [{char}]")

    def handle_string(self, char):
        if char == "\n" or char == None:
            raise InvalidTokenError(
                "Expected a \" for termination while new-line or null terminated character was read")
        elif char == "\"":
            self.add_token(Str("".join(self.char_buffer)))
            self.char_buffer.clear()
            self.current_state = State.GENERAL
        else:
            self.char_buffer.append(char)

    def handle_number(self, char):
        if self.is_number_end(char):
            self.add_token(Num(int("".join(self.char_buffer))))
            self.char_buffer.clear()
            self.current_state = State.GENERAL
            self.handle_general(char)
        elif char.isdigit():
            self.char_buffer.append(char)
        else:
            raise InvalidTokenError(
                f"Expected a number while invalid character [{char}] was read")

    def is_number_end(self, char):
        return char in self.spacing_characters or char in self.brackets or char == ',' or char == '\n' or char == None

    def handle_identifier(self, char):
        if self.is_identifier_end(char):
            name = "".join(self.char_buffer)
            self.char_buffer.clear()
            self.current_state = State.GENERAL
            if name in RESERVED_NAME:
                self.add_token(Reserved(name))
            else:
                self.add_token(Var(name))
            self.handle_general(char)
        elif char.isdigit() or char.isalpha or char == '_':
            self.char_buffer.append(char)
        else:
            raise InvalidTokenError(
                f"Expected a number, letter or underscore while invalid character [{char}] was read")

    def is_identifier_end(self, char):
        return char in self.spacing_characters or char in self.brackets or char == '=' or char == '\n' or char == None

    def add_token(self, token):
        self.list_of_tokens.append(token)
