"""
   Filename:  glpk_lex.py (Python parser for GnuMathProg language)

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

import re
import ply.lex as lex
import ply.yacc as yacc

# Get the token map from the lexer.
from glpk_lex import *
from model_objects import *

class regexcache:
    def __init__(self):
        self.cache = {}
    def __getitem__(self, pattern):
        if pattern not in self.cache:
            rgx = re.compile(pattern,re.X)
            self.cache[pattern] = rgx
        else:
            rgx = self.cache[pattern]
        return rgx

regex = regexcache()

non_scolon = r'''(?:(?:\".*?\"|\'.*?\'|[^;])*;)'''

class glpk_parser:
    def __init__(self, mod_file, dat_file = None):
        try:
            fmod = open(mod_file)
            self.mod = fmod.read()
        except:
            self.mod = ""
        try:
            fdat = open(dat_file)
            self.dat = fdat.read()
        except:
            self.dat = None
        self.parse()
        
    def __getitem__(self, name):
        return self.__dict__[name]
        
    def __setitem__(self, name, value):
        self.__dict__[name] = value

    def parse_data_decls(self, ldat):
        defaults = {} # parameters default values

        pattern = r'(param)\s+(\w+)\s*((default)\s*(\w*))?'
        rgx_param = regex[pattern]
        
        pattern = r'(param)\s*((default)\s*([^\s]))?\s*(:[^:]*)?:([^:]*):'
        rgx_param_tab = regex[pattern]

        for decl in ldat:
            m = rgx_param_tab.match(decl)
            if m != None:
                lst = m.group(6).split()
                for name in lst:
                    defval = m.group(4)
                    if defval:
                        defaults[name] = defval
                continue

            m = rgx_param.match(decl)
            if m != None:
                name = m.group(2)
                defval = m.group(5)
                if defval:
                    defaults[name] = defval
                continue            
        self.default_values = defaults

    def parse_model_decls(self, lmod):
        types = {}  # set/param/var
        values = {} # {}/None
        names = []
        
        pattern = r'''(?:(set|param|var|subject\s*to|s.t.|minimize|maximize)\s+)?
                      (\w*)\s*(\"(?:[^\"]|\"\")*\"|\'(?:[^\']|\'\')*\')?
                      \s*(\{[^}]*\})?.*'''
        rgx = regex[pattern]
        
        for decl in lmod:
            m = rgx.match(decl)
            if m != None:
                _type = m.group(1)
                if _type == None:
                    _type = 's.t.'
                _name = m.group(2)
                _domain = m.group(4)
                names.append(_name)
                if _type == 's.t.':
                    types[_name] = 'constraint'
                if _type.startswith('subject'):
                    types[_name] = 'constraint'
                elif _type in ['maximize','minimize']:
                    types[_name] = 'objective'
                elif _type == 'set' and ':=' in decl:
                    types[_name] = 'setx'
                else:
                    types[_name] = _type
                if _domain!=None:
                    values[_name] = {}
                else:
                    values[_name] = None                                       
                    
        self.names = names
        self.types = types
        self.values = values
        
    def parse(self):
        mod = self.mod
        dat = self.dat
        lmod = []
        ldat = []
        
        # remove comments (#... and /*...*/)
        pattern = r'''(\".*?\"|\'.*?\'|/\*.*?\*/|\#.*)'''
        rgx = regex[pattern]
        def comrepl(match):
            s = match.group(0)
            if s[0] in '/#': return ''
            else: return s
        mod = rgx.sub(comrepl,mod)
        if dat != None:
            dat = rgx.sub(comrepl,dat)
        
        # parse model file
        pattern = r'[A-Za-z_]'+ non_scolon
        rgx = regex[pattern]
        tmod = rgx.findall(mod)

        # read data section
        i, n = 0, len(tmod)
        set_dacls = {}
        param_decls = {}
        while i < n:
            if tmod[i].startswith('data'):
                i += 1
                ldat = []
                while i < n and not tmod[i].startswith('end'):
                    ldat.append(tmod[i])
                    i += 1
                i += 1
            else:
                if tmod[i].replace(' ','') != 'end;':
                    lmod.append(tmod[i])
                i += 1

        # parse data file
        if dat != None:
            pattern = r'''set(?:(?:\".*?\"|\'.*?\'|[^;])*;)
                        | param(?:(?:\".*?\"|\'.*?\'|[^;])*;)'''
            rgx = regex[pattern]
            ldat = rgx.findall(dat)

        # parse model decls
        self.parse_model_decls(lmod)            
            
        # parse data decls
        self.parse_data_decls(ldat)
        
        # store model
        s = ""
        for decl in lmod:
            s += decl+'\n'
        self.model = s

        self.lmod = lmod
        self.ldat = ldat
                        
    def generate_model(self, filename):
        s = ""
        lmod = self.lmod
        ldat = self.ldat
        types = self.types
        for x in lmod:
            if x.startswith('set') or x.startswith('var') or x.startswith('param'):
                s += x+'\n'
        for x in types:
            if types[x] in ['set','setx','param']:
                s += "display %s;\n" % x
        s += "data;\n"
        for decl in ldat:
            s += decl+'\n'
        s += "end;"
        f = open(filename, "w")
        print >>f, s

def load_data(parser, outputfile, glpkobj):    
    text = open(outputfile).read()
    pattern = r'''Display\sstatement\sat\sline\s[0-9]+
                | \w+\shas\sempty\scontent
                | \w+\sis\sempty'''
    rgx = regex[pattern]
    text = rgx.sub('', text)
    rgx = regex[r'(\w+)\s*(\=|\:)']
    text = rgx.sub(r'>>> \1 \2', text)
    rgx = regex[r'(\w+)\s*(\[.*?\])\s*(\=|\:)']
    text = rgx.sub(r'>>> \1\2 \3', text)
    lst = yacc.parse(text)
    
    for x in parser.names:
        _type = parser.types[x]
        _value = parser.values[x]
        glpkobj._type[x] = _type
        if _type == 'var':    
            glpkobj[x] = var(glpkobj, x, _value)
        elif _type == 'constraint':
            glpkobj[x] = constraint(glpkobj, x, _value)
        elif _type == 'objective':
            glpkobj[x] = objective(glpkobj, x, _value)
        else:
            glpkobj[x] = _value 

    for (_name, _ind, _val) in lst:
        if _ind == None:
            glpkobj[_name] = _val
        else:
            glpkobj[_name][_ind] = _val 
            
    glpkobj._model = parser.model
    glpkobj._default = parser.default_values
    
    glpkobj._sets_names = []
    glpkobj._vars_names = []
    glpkobj._params_names = []
    glpkobj._constraints_names = []
    glpkobj._objectives_names = []
    for x in parser.names:
        typ = parser.types[x]
        if typ == 'set':
            glpkobj._sets_names.append(x)
        elif typ == 'param':
            glpkobj._params_names.append(x)
        elif typ == 'var':
            glpkobj._vars_names.append(x)
        elif typ == 'constraint':
            glpkobj._constraints_names.append(x)
        elif typ == 'objective':
            glpkobj._objectives_names.append(x)

def load_solution(solution, glpkobj):
    s = ""
    for x in solution:
        s +=  ">>> %s = %s\n" % (x,float(solution[x]))
    lst = yacc.parse(s)
    for (_name, _ind, _val) in lst:
        if _ind == None:
            try:
                glpkobj[_name]._value = _val     
            except:
                glpkobj[_name] = var(glpkobj, _name, _val)
        else:
            glpkobj[_name][_ind]._value = _val
            

def p_data(p):
    '''data : data decl
            |''' 
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])
                    
def p_decl(p):
    '''decl : PROMPT set
            | PROMPT param'''
    p[0] = p[2]

def p_name(p):
    '''name : STRING
            | STRING tuple'''
    if len(p) == 2:
        p[0] = (p[1],None)
    else:
        if len(p[2])==1:
            p[2] = p[2][0]
        p[0] = (p[1],p[2])

def p_set(p):
    '''set :  name ':' list'''
    p[0] = (p[1][0],p[1][1],p[3])

def p_param(p):
    '''param : name '=' record'''
    p[0] = (p[1][0],p[1][1],p[3])

def p_list(p):
    '''list : record
            | list record'''
    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])

def p_tuple(p):
    '''tuple : LPAREN list RPAREN
             | LBRACK list RBRACK'''
    p[0] = tuple(p[2])
    
def p_record(p):
    '''record : FLOAT
              | INTEGER
              | STRING
              | tuple'''          
    p[0] = p[1]

def p_error(p):
    # Error rule for syntax errors
    print "[",p,"]"
    print "<",p.value,">"
    print "Syntax error in input!"
    import sys
    sys.exit(0)



def show_tokens():
    while True:
        tok = lexer.token()
        if not tok: break
        print tok

# Build the parser
yacc.yacc(write_tables=0, debug=0)

