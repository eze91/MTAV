"""
   Filename:  glpk_lex.py (Python lexer for GnuMathProg language)

-- This code is part of the Python-GLPK interface.
--
-- Copyright (C) 2005, Joao Pedro Pedroso and Filipe Brandao
-- Faculdade de Ciencias, Universidade do Porto
-- Porto, Portugal. All rights reserved. E-mail: <jpp@fc.up.pt>.
--
-- Python-GLPK is free software; you can redistribute it and/or modify it
-- under the terms of the GNU General Public License as published by the
-- Free Software Foundation; either version 2, or (at your option) any
-- later version.
--  
-- Python-GLPK is distributed in the hope that it will be useful, but
-- WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
-- General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with GLPK; see the file COPYING. If not, write to the Free
-- Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
-- 02110-1301, USA.
"""

import ply.lex as lex
import re

reserved = {}

# List of token names.   This is always required
tokens = [
   'LPAREN',
   'RPAREN',
   'LBRACK',
   'RBRACK',
   'STRING',
   'INTEGER',
   'FLOAT',
   'PROMPT',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_PROMPT = r'>>>'

literals = ":;=,"

def t_STRING(t):
    r'''[a-zA-Z_0-9]*[a-zA-Z_+][a-zA-Z_\+\-0-9]*
        | [a-zA-Z_][a-zA-Z_\+\-0-9]* 
        | [a-zA-Z_\+\-0-9]*[a-zA-Z_]
        | \'([^\']|\'\')*\' | \"([^\"]|\"\")*\" '''
    t.value = t.value.strip('\'\"\n')
    t.value = t.value.replace('\'','')
    t.value = t.value.replace('\"','')
    return t

def t_FLOAT(t):
    r'''[\+\-]?[0-9]*[\.]?[0-9]*([eE][\-\+]?[0-9]+) 
        | [\+\-]?[0-9]*\.[0-9]+'''
    t.value = float(t.value)
    return t
    
def t_INTEGER(t):
    r'[\+\-]?\d+'
    t.value = int(t.value)    
    return t



# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters
t_ignore  = ' \r\t,'

# Error handling rule
def t_error(t):
    print "Illegal character %s" % repr(t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
#lexer = lex.lex(optimize=1)


