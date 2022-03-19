import re

import ply.lex
import ply.yacc

states = (
    ("unorderedlist", "inclusive"),
    ("blockquote", "inclusive"),
    ("numberedlist", "inclusive")
)

tokens = (

    "ESCAPED_CHAR",

    "HEADER_ONE",
    "HEADER_TWO",
    "HEADER_THREE",
    "HEADER_FOUR",
    "HEADER_FIVE",
    "HEADER_SIX",

    "HEADER_ONE_ALT",
    "HEADER_TWO_ALT",

    "BOLD_TEXT",
    "BOLD_TEXT_UL",
    "MONOSPACE_TEXT",
    "ITALIC_TEXT",
    "ITALIC_TEXT_UL",

    "INDENT_BLOCK_START",
    "INDENT_BLOCK_END",

    "NUMBERED_LIST_START",
    "NUMBERED_LIST_ITEM",
    "NUMBERED_LIST_END",

    "UNORDERED_LIST_START",
    "UNORDERED_LIST_ITEM",
    "UNORDERED_LIST_END",

    "DOUBLE_NEW_LINE",

    "WORD_SEPERATOR",
    "NEW_LINE",
    "CHAR",
    "UNICODE_CHAR",
    "NOT_CHAR",
)


t_DOUBLE_NEW_LINE = (
    r'\n\n'
)




def t_ESCAPED_CHAR(t):
    r"\\."
    p = r"\\(.)"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_ONE(t):
    r"\n\#\s(.*)+\n"
    p = r"\n\# (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_ONE_ALT(t):
    r'\n([\w \S]+)\n[==]+\n'
    p = r'\n([\w \S]+)\n[==]+\n'
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_TWO(t):
    r"\n\#\#\s(.*)\n"
    p = r"\n[\#]+ (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_TWO_ALT(t):
    r'\n([\w \S]+)\n[\-\-]+\n'
    p = r'\n([\w \S]+)\n[\-\-]+\n'
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_THREE(t):
    r"\n\#\#\#\s(.*)\n"
    p = r"\n[\#]+ (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_FOUR(t):
    r"\n\#\#\#\#\s(.*)\n"
    p = r"\n[\#]+ (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_FIVE(t):
    r"\n\#\#\#\#\#\s(.*)\n"
    p = r"\n[\#]+ (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


def t_HEADER_SIX(t):
    r"\n\#\#\#\#\#\#\s(.*)\n"
    p = r"\n[\#]+ (.*)\n"
    t.value = re.match(p, t.value).group(1)
    return t


orig_t_unorderedlist_UNORDERED_LIST_ITEM = (
    r"\n[ ]+\*[ ]+"
)


def t_UNORDERED_LIST_START(t):
    r"\n[ ]+\*[ ]+(.*)\n"
    p = r"\n[ ]+\*[ ]+(.*)\n"
    t.lexer.push_state("unorderedlist")
    t.value = re.match(p, t.value).group(1)
    return t

def t_unorderedlist_UNORDERED_LIST_ITEM(t):
    r"[ ]+\*[ ]+(.*)\n"
    p = r"[ ]+\*[ ]+(.*)\n"
    t.value = re.match(p, t.value).group(1)
    #print("UNORDERED LIST NEXT VAL {}".format(t.value))
    return t


def t_unorderedlist_UNORDERED_LIST_END(t):
    r"[\s]*[^\*]"
    t.lexer.pop_state()
    #print("UNORDERED LIST END VAL")
    return t


def t_NUMBERED_LIST_START(t):
    r"\n[ ]+[\d]\.[ ]+(.*)\n"
    p = r"\n[ ]+[\d]\.[ ]+(.*)\n"
    t.lexer.push_state("numberedlist")

    t.value = re.match(p, t.value).group(1)
    #print("NUMBERED LIST START VAL {}".format(t.value))
    return t

def t_numberedlist_NUMBERED_LIST_ITEM(t):
    r"[ ]+[\d]\.[ ]+(.*)\n"
    p = r"[ ]+[\d]\.[ ]+(.*)\n"

    t.value = re.match(p, t.value).group(1)
    #print("NUMBERED LIST NEXT VAL {}".format(t.value))
    return t


def t_numberedlist_NUMBERED_LIST_END(t):
    r"[\s]*[\D]"
    t.lexer.pop_state()
    #print("NUMBERED LIST END VAL")
    return t


def t_ITALIC_TEXT(t):
    r" \*[^\*\n]+\*"
    p = "\*(.*)\*"
    t.value = re.match(p, t.value).group(1)
    return t


def t_ITALIC_TEXT_UL(t):
    r"_[^_\n]+_"
    p = "_(.*)_"
    t.value = re.match(p, t.value).group(1)
    return t


def t_BOLD_TEXT(t):
    r"\*\*.*\*\*"
    p = r'\*\*(.*)\*\*'
    t.value = re.match(p, t.value).group(1)
    return t


def t_BOLD_TEXT_UL(t):
    r"__.*__"
    p = r'__(.*)__'
    t.value = re.match(p, t.value).group(1)
    return t


def t_MONOSPACE_TEXT(t):
    r" `(.*)` "
    p = r"`(.*)`"
    t.value = re.match(p, t.value).group(1)
    return t


def t_INDENT_BLOCK_START(t):
    r"\n[>]+[\s]"
    t.lexer.push_state("blockquote")
    return t


def t_blockquote_INDENT_BLOCK_START(t):
    r"\n[>]+[\s]"
    return None


def t_blockquote_INDENT_BLOCK_END(t):
    r'\n\n'
    t.lexer.pop_state()
    return t


t_NOT_CHAR = (
    r"\W"
)

t_CHAR = (
    r"\w"
)

t_WORD_SEPERATOR = (
    r"[ \t]"
)

t_NEW_LINE = (
    r"[\r\n]"

)


def t_error(t):
    raise TypeError("Unknown text '%s' %s" % (t.value[0], hex(ord(t.value[0]))))


ply.lex.lex(reflags=re.UNICODE | re.VERBOSE)

with open("example_markdown.md") as test_markdown_file:
    test_markdown = test_markdown_file.read()


def p_header_one(p):
    '''
    html_text :  HEADER_ONE
              |  HEADER_ONE_ALT
              |  html_text HEADER_ONE_ALT
              |  html_text HEADER_ONE

    '''
    if len(p) > 2:
        tagged_header = "<h1>{}</h1>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h1>{}</h1>".format(p[1])
        p[0] = tagged_header


def p_header_two(p):
    '''
    html_text :  HEADER_TWO
              |  HEADER_TWO_ALT
              |  html_text HEADER_TWO_ALT
              |  html_text HEADER_TWO
    '''
    if len(p) > 2:
        tagged_header = "<h2>{}</h2>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h2>{}</h2>".format(p[1])
        p[0] = tagged_header


def p_header_three(p):
    '''
    html_text :  HEADER_THREE
              |  html_text HEADER_THREE
    '''
    if len(p) > 2:
        tagged_header = "<h3>{}</h3>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h3>{}</h3>".format(p[1])
        p[0] = tagged_header


def p_header_four(p):
    '''
    html_text :  HEADER_FOUR
              |  html_text HEADER_FOUR
    '''
    if len(p) > 2:
        tagged_header = "<h4>{}</h4>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h4>{}</h4>".format(p[1])
        p[0] = tagged_header


def p_header_five(p):
    '''
    html_text :  HEADER_FIVE
              |  html_text HEADER_FIVE
    '''
    if len(p) > 2:
        tagged_header = "<h5>{}</h5>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h5>{}</h5>".format(p[1])
        p[0] = tagged_header


def p_header_six(p):
    '''
    html_text :  HEADER_SIX
              |  html_text HEADER_SIX
    '''
    if len(p) > 2:
        tagged_header = "<h6>{}</h6>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_header)
    else:
        tagged_header = "<h6>{}</h6>".format(p[1])
        p[0] = tagged_header


def p_new_line(p):
    '''
    html_text : NEW_LINE
              | html_text NEW_LINE
    '''
    if len(p) > 2:
        p[0] = "{}\n".format(p[1])
    else:
        p[0] = "\n"


def p_italics_text(p):
    '''
    html_text : ITALIC_TEXT
              | html_text ITALIC_TEXT
              | html_text ITALIC_TEXT_UL
              | ITALIC_TEXT_UL
    '''
    if len(p) > 2:
        tagged_text = "<i>{}</i>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_text)
    else:
        tagged_text = "<i>{}</i>".format(p[1])
        p[0] = tagged_text


def p_monospace_text(p):
    '''
    html_text : MONOSPACE_TEXT
              | html_text MONOSPACE_TEXT
    '''
    if len(p) > 2:
        tagged_text = "<tt>{}<tt>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_text)
    else:
        tagged_text = "<tt>{}</tt>".format(p[1])
        p[0] = tagged_text


def p_bold_text(p):
    '''
    html_text : BOLD_TEXT
              | html_text BOLD_TEXT
              | BOLD_TEXT_UL
              | html_text BOLD_TEXT_UL

    '''
    if len(p) > 2:
        tagged_text = "<b>{}<b>".format(p[2])
        p[0] = "{}{}".format(p[1], tagged_text)
    else:
        tagged_text = "<b>{}</b>".format(p[1])
        p[0] = tagged_text


def p_block_text_start(p):
    '''
    html_text : INDENT_BLOCK_START
              | html_text INDENT_BLOCK_START
    '''
    if len(p) > 2:
        tagged_text = "<pre>"
        p[0] = "{}{}".format(p[1], tagged_text)
    else:
        tagged_text = "<pre>"
        p[0] = tagged_text


def p_block_text_end(p):
    '''
    html_text : html_text INDENT_BLOCK_END
    '''
    p[0] = "{}</pre>".format(p[1])


def p_numbered_list_start(p):
    '''
    html_text : html_text NUMBERED_LIST_START
    '''
    p[0] = "{}<ol>\n<li>{}</li>\n".format(p[1], p[2])


def p_numbered_list_item(p):
    '''
    html_text : html_text NUMBERED_LIST_ITEM
    '''
    p[0] = "{}\n<li>{}</li>\n".format(p[1], p[2])


def p_numbered_list_end(p):
    '''
    html_text : html_text NUMBERED_LIST_END
    '''
    p[0] = "{}<ol>\n".format(p[1])


def p_unordered_list_start(p):
    '''
    html_text : html_text UNORDERED_LIST_START
    '''
    p[0] = "{}<ul>\n<li>{}</li>\n".format(p[1], p[2])


def p_unordered_list_item(p):
    '''
    html_text : html_text UNORDERED_LIST_ITEM
    '''
    p[0] = "{}\n<li>{}</li>\n".format(p[1], p[2])


def p_unordered_list_end(p):
    '''
    html_text : html_text UNORDERED_LIST_END
    '''
    p[0] = "{}<ul>\n".format(p[1])



def p_char(p):
    '''
    html_text : CHAR
              | html_text CHAR
              | NOT_CHAR
              | html_text NOT_CHAR
              | WORD_SEPERATOR
              | html_text WORD_SEPERATOR
              | ESCAPED_CHAR
              | html_text ESCAPED_CHAR
    '''
    if len(p) > 2:
        p[0] = "{}{}".format(p[1],p[2])
    else:
        p[0] = p[1]


def p_error(p):
    print(p)
    print("Syntax error at '%s'" % p.value)


ply.lex.lex(reflags=re.UNICODE | re.VERBOSE)
parser = ply.yacc.yacc()

with open("example_markdown.md") as test_markdown_file:
    test_markdown = test_markdown_file.read()

#ply.lex.input(test_markdown)

#for tok in iter(ply.lex.token, None):
#    print(repr(tok.type), repr(tok.value))

out = parser.parse(test_markdown)
print(out)