from typing import List
import sys

token_map = {
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    ",": "COMMA",
    ".": "DOT",
    "-": "MINUS",
    "+": "PLUS",
    ";": "SEMICOLON",
    "*": "STAR",
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "fun": "FUN",
    "for": "FOR",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE",
    "!": "BANG",
    "!=": "BANG_EQUAL",
    "=": "EQUAL",
    "==": "EQUAL_EQUAL",
    ">": "GREATER",
    ">=": "GREATER_EQUAL",
    "<": "LESS",
    "<=": "LESS_EQUAL",
    '"': "STRING",
    "/": "SLASH",
}
IGNORE = ["\t", " "]
special_tokens = ["=", ">", "<", "!", "/"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


class Token:
    def __init__(
        self, token: str, line: int, literal: str = "", valid: bool = True
    ) -> None:
        self.token = token
        self.literal = literal
        self.disc = "null"
        self.line: int = line
        self.valid: bool = valid

    def __repr__(self) -> str:
        return f"{self.token}  {self.literal}"

    def error_output(self):
        sys.stderr.write(
            f"[line {self.line}] Error: Unexpected character: {self.token}\n"
        )

    def valid_output(self):
        sys.stdout.write(f"{self.literal} {self.token} {self.disc}\n")

    def display_tokens(self):
        if self.valid:
            self.valid_output()
        else:
            self.error_output()


class StringToken(Token):
    def __init__(self, line: int, literal: str = "STRING", valid: bool = True) -> None:
        super().__init__('"', line, literal, valid)
        self.value = ""

    def error_output(self):
        sys.stderr.write(f"[line {self.line}] Error: Unterminated string.")

    def valid_output(self):
        sys.stdout.write(f'{self.literal} "{self.value}" {self.value}\n')


class IntToken(Token):
    def __init__(self, line: int, literal: str = "NUMBER", valid: bool = True) -> None:
        super().__init__("", line, literal, valid)
        self.value = ""

    def error_output(self):
        sys.stderr.write(f"Ops")

    def valid_output(self):
        sys.stdout.write(f"{self.literal} {self.value} {float(self.value)}\n")


class Scanner:
    def __init__(self, source: str) -> None:
        self.tokens: List[Token] = []
        self.source: str = source
        self.index: int = 0
        self.line: int = 1
        self.status_code: int = 0

    def print(self):
        token: Token
        for token in self.tokens:
            token.display_tokens()

    def scanTokens(self):
        while not self.is_at_end():
            match self.source[self.index]:
                case "\n":
                    self.line += 1
                    self.advance()
                case '"':
                    self.string_literal()
                    self.advance()
                case token if token in numbers:
                    self.number_literal()
                case token if token in IGNORE:
                    self.advance()
                case token if token in special_tokens:
                    composite_index = self.token_need_special_care(token)

                    if composite_index == "//":
                        pass
                    elif composite_index in token_map.keys():
                        self.add_token(composite_index)
                    else:
                        self.add_token(self.source[self.index])
                    self.advance()
                case _:
                    self.add_token(self.source[self.index])
                    self.advance()

        self.tokens.append(Token(token="", literal="EOF", line=self.line))

    def number_literal(self):
        int_token = IntToken(self.line)

        while (
            not self.is_at_end()
            and self.token != "\n"
            and (self.token in numbers or self.token == ".")
        ):
            int_token.value += self.token

            self.advance()

        self.tokens.append(int_token)

    def string_literal(self):
        string_token = StringToken(self.line)
        self.advance()

        while not self.is_at_end() and self.token != '"' and self.token != "\n":
            string_token.value += self.token
            self.advance()
        if self.is_at_end() or self.token == "\n":
            string_token.valid = False
            self.status_code = 65

        self.tokens.append(string_token)

    @property
    def token(self):
        return self.source[self.index]

    def is_at_end(self) -> bool:
        return self.index >= len(self.source)

    def advance_until_eol(self):
        while not self.is_at_end() and self.source[self.index] != "\n":
            self.advance()
        self.line += 1

    def advance(self):
        self.index += 1

    def add_token(self, token: str):
        token_data = {
            "token": token,
            "line": self.line,
            "valid": True,
        }

        if token in token_map.keys():
            token_data["literal"] = token_map[token]
        else:
            token_data["valid"] = False
            self.status_code = 65

        self.tokens.append(Token(**token_data))

    def token_need_special_care(self, token: str):
        next_token = self.get_next_token()
        special_token = f"{token}{next_token}"

        if special_token == "//":
            self.advance()
            self.advance_until_eol()
        elif special_token in token_map.keys():
            self.advance()
        return special_token

    def get_next_token(self):
        if len(self.source) == 1 or len(self.source) == self.index + 1:
            return None
        elif not self.is_at_end():
            return self.source[self.index + 1]
        return None


if __name__ == "__main__":
    print("Hello")
