from os import linesep
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


class Token:
    def __init__(
        self, name: str, line: int, literal: str = "", valid: bool = True
    ) -> None:
        self.name = name
        self.litheral = literal
        self.disc = "null"
        self.line: int = line
        self.valid: bool = valid

    def __repr__(self) -> str:
        return f"{self.name}  {self.litheral}"


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
            if token.valid:
                sys.stdout.write(f"{token.litheral} {token.name} {token.disc}\n")
            else:
                sys.stderr.write(
                    f"[line {token.line}] Error: Unexpected character: {token.name}\n"
                )

    def scanTokens(self):
        while not self.is_at_end():
            match self.source[self.index]:
                case "\n":
                    self.line += 1
                case token if token in IGNORE:
                    pass
                case token if token in special_tokens:
                    composite_index = self.token_need_special_care(token)

                    if composite_index == "//":
                        pass
                    elif composite_index in token_map.keys():
                        self.add_token(composite_index)
                    else:
                        self.add_token(self.source[self.index])
                case _:
                    self.add_token(self.source[self.index])
            self.advance()

        self.tokens.append(Token(name="", literal="EOF", line=self.line))

    def is_at_end(self) -> bool:
        if self.index >= len(self.source):
            return True
        return False

    def advance_until_eol(self):
        while not self.is_at_end() and self.source[self.index] != "\n":
            self.advance()
        self.line += 1

    def advance(self):
        self.index += 1

    def add_token(self, token: str):
        token_data = {
            "name": token,
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
        if len(self.source) == 1:
            return None
        elif len(self.source) == self.index + 1:  # we are the end of string
            return None
        elif not self.is_at_end():
            return self.source[self.index + 1]
        return None


if __name__ == "__main__":
    print("Hello")
