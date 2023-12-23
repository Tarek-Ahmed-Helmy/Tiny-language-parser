import pydot
import random

"""
# Grammar for TINY:
program → stmt-sequence
stmt-sequence → stmt-sequence ; statement | statement
statement → if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
if-stmt → if exp then stmt-sequence end
repeat-stmt → repeat stmt-sequence until exp
assign-stmt → identifier := exp
read-stmt → read identifier
write-stmt → write exp
exp → simple-exp comparison-op simple-exp | simple-exp
comparison-op → < | =
simple-exp → simple-exp addop term | term
addop → + | -
term → term mulop factor | factor
mulop → * | /
factor → (exp) | number | identifier

# EBNF
program → stmt-sequence
stmt-sequence → statement {; statement}
statement → if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
if-stmt → if exp then stmt-sequence end
repeat-stmt → repeat stmt-sequence until exp
assign-stmt → identifier := exp
read-stmt → read identifier
write-stmt → write exp
exp → simple-exp [comparison-op simple-exp]
comparison-op → < | =
simple-exp → term {addop term}
addop → + | -
term → factor {mulop factor}
mulop → * | /
factor → (exp) | number | identifier
"""


class Parser:
    def __init__(self, tokens_table):
        self.tokens_table = tokens_table
        self.counter = 0
        self.max_counter = len(tokens_table)
        self.syntax_tree = pydot.Dot(graph_type='graph', rankdir="TB")
        self.id_counter = 0

    def match(self, expected_token):
        if self.counter == self.max_counter:
            return 0  # error-end-of-tokens

        if self.tokens_table[self.counter][1] == expected_token:
            token_val = self.tokens_table[self.counter][0]
            self.counter = self.counter + 1
            return token_val  # match-found
        else:
            return 0  # error-no-match

    # stmt-sequence → statement {; statement}
    def stmt_sequence(self):
        stmt_node = self.statement()
        temp_node = stmt_node
        while self.match("SEMICOLON"):
            stmt_node_n = self.statement()
            # to be connected horizontally
            self.syntax_tree.add_edge(pydot.Edge(temp_node, stmt_node_n, constraint=False, color='#FF0000'))
            temp_node = stmt_node_n

        self.syntax_tree.write_png("syntax_tree.png")
        return stmt_node

    # statement→ if-stmt | repeat-stmt | assign-stmt | read-stmt | write-stmt
    def statement(self):
        if self.match("IF"):
            return self.if_stmt()

        elif self.match("REPEAT"):
            return self.repeat_stmt()

        elif self.match("READ"):
            return self.read_stmt()

        elif self.match("WRITE"):
            return self.write_stmt()

        elif self.match("IDENTIFIER"):
            return self.assign_stmt()

        else:
            raise Exception("No match found")

    # if-stmt → if exp then stmt-sequence [else stmt-sequence] end
    def if_stmt(self):
        if_node = pydot.Node(str(self.id_counter), label=f"if", shape="rect", rank="same")
        self.syntax_tree.add_node(if_node)
        self.id_counter = self.id_counter + 1
        exp_node = self.exp()
        if self.match("THEN"):
            then_node = self.stmt_sequence()
            self.syntax_tree.add_edge(pydot.Edge(if_node, exp_node))
            self.syntax_tree.add_edge(pydot.Edge(if_node, then_node))

        else:
            raise Exception("No match found")

        if self.match("ELSE"):
            else_node = self.stmt_sequence()
            self.syntax_tree.add_edge(pydot.Edge(if_node, else_node, style="dotted"))

        if not self.match("END"):
            raise Exception("No match found")

        return if_node

    # repeat-stmt → repeat stmt-sequence until exp
    def repeat_stmt(self):
        repeat_node = pydot.Node(str(self.id_counter), label=f"repeat", shape="rect", rank="same")
        self.syntax_tree.add_node(repeat_node)
        self.id_counter = self.id_counter + 1
        stmt_node = self.stmt_sequence()
        if self.match("UNTIL"):
            exp_node = self.exp()
            self.syntax_tree.add_edge(pydot.Edge(repeat_node, stmt_node))
            self.syntax_tree.add_edge(pydot.Edge(repeat_node, exp_node))
        else:
            raise Exception("No match found")

        return repeat_node

    # read-stmt → read identifier
    def read_stmt(self):
        ID = self.match("IDENTIFIER")
        if ID:
            read_node = pydot.Node(str(self.id_counter), label=f"read\n({ID})", shape="rect", rank="same")
            self.syntax_tree.add_node(read_node)
            self.id_counter = self.id_counter + 1
            return read_node
        else:
            raise Exception("No match found")

    # write-stmt → write exp
    def write_stmt(self):
        write_node = pydot.Node(str(self.id_counter), label=f"write", shape="rect", rank="same")
        self.syntax_tree.add_node(write_node)
        self.id_counter = self.id_counter + 1
        stmt_node = self.exp()
        self.syntax_tree.add_edge(pydot.Edge(write_node, stmt_node))
        return write_node

    # assign-stmt → identifier := exp
    def assign_stmt(self):
        ID = self.tokens_table[self.counter - 1][0]
        assign_node = pydot.Node(str(self.id_counter), label=f"assign\n({ID})", shape="rect", rank="same")
        self.syntax_tree.add_node(assign_node)
        self.id_counter = self.id_counter + 1
        if self.match("ASSIGN"):
            node = self.exp()
            self.syntax_tree.add_edge(pydot.Edge(assign_node, node))
            return assign_node
        else:
            raise Exception("No match found")

    # exp → simple-exp [comparison-op simple-exp]
    # comparison-op → < | =
    def exp(self):
        simple_exp_node = self.simple_exp()
        if self.match("LESSTHAN") or self.match("EQUAL"):
            op = self.tokens_table[self.counter - 1][0]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            simple_exp_node2 = self.simple_exp()
            self.syntax_tree.add_edge(pydot.Edge(op_node, simple_exp_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node, simple_exp_node2))
            simple_exp_node = op_node

        return simple_exp_node

    # simple-exp → term {addop term}
    # addop → + | -
    def simple_exp(self):
        term_node = self.term()
        while self.match("PLUS") or self.match("MINUS"):
            op = self.tokens_table[self.counter - 1][0]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            term_node2 = self.term()
            self.syntax_tree.add_edge(pydot.Edge(op_node, term_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node, term_node2))
            term_node = op_node

        return term_node

    # term → factor {mulop factor}
    # mulop → * | /
    def term(self):
        factor_node = self.factor()
        while self.match("MULT") or self.match("DIV"):
            op = self.tokens_table[self.counter - 1][0]
            op_node = pydot.Node(str(self.id_counter), label=f"op\n({op})")
            self.syntax_tree.add_node(op_node)
            self.id_counter = self.id_counter + 1
            factor_node2 = self.factor()
            self.syntax_tree.add_edge(pydot.Edge(op_node, factor_node))
            self.syntax_tree.add_edge(pydot.Edge(op_node, factor_node2))
            factor_node = op_node

        return factor_node

    # factor → (exp) | number | identifier
    def factor(self):
        if self.match("OPENBRACKET"):
            exp_node = self.exp()
            if not self.match("CLOSEDBRACKET"):
                raise Exception("No match found")
            return exp_node
        elif self.match("NUMBER"):
            const = self.tokens_table[self.counter - 1][0]
            const_node = pydot.Node(str(self.id_counter), label=f"const\n({const})")
            self.id_counter = self.id_counter + 1
            self.syntax_tree.add_node(const_node)
            return const_node

        elif self.match("IDENTIFIER"):
            ID = self.tokens_table[self.counter - 1][0]
            id_node = pydot.Node(str(self.id_counter), label=f"id\n({ID})")
            self.syntax_tree.add_node(id_node)
            self.id_counter = self.id_counter + 1
            return id_node

        else:
            raise Exception("No match found")
