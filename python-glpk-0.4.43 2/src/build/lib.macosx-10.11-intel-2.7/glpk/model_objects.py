"""
   Filename:  model_objects.py (tools for processing GnuMathProg language)

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

def name_to_index(name):
    if type(name)==tuple:
        s = ''
        for i in range(len(name)):
            if i>0: s += ','
            if type(name[i])==str:
                if ',' not in name[i]:
                    t = name[i]
                else:
                    t = "'%s'" % (name[i])
            else:
                t = str(name[i])
            s += t
        return s
    else:
        return name

def join_bounds(cur, new):
    if cur == None:
        return new
    if new == None:
        return cur
    if new[0] == '=':
        return new
    else:
        cur = list(cur)
        if cur[0] == '=':
            cur = (None, None)
        if new[0] != None:
            cur[0] = new[0]
        if new[1] != None:
            cur[1] = new[1]
        return tuple(cur)
        
class var:
    def __init__(self, prob, name, value = None, bnds = None):
        self._prob = prob
        self._name = name
        self._subvars = None
        if type(value) != dict:
            self._value = value
        else:
            self._subvars = value

    def value(self):
        return self._value                     

    def _bounds(self):
        try:
            bnds = self._prob._bounds[self._name]
        except:
            bnds = None
        return bnds

    def _clear(self):
        self._prob._rm_bounds(self._name)                  
        
    def __del__(self):
        self.clear()
                
    def _set_bounds(self, bounds):
        self._prob._set_bounds(self._name, bounds)
        if self._subvars:
          for x in self:
            self[x]._set_bounds(bounds)
        
    def __eq__(self, value):
        self._set_bounds(('=', value))
        for x in self:
            self[x] == value
        return nothing()
        
    def __ge__(self, value):
        self._set_bounds(('>=', value))
        return nothing()
        
    def __le__(self, value):
        self._set_bounds(('<=', value))
        return nothing()
               
    def __str__(self):
        if self._subvars == None:
            return '(var:'+str(self._value)+')'
        else:
            return '(var:'+str(self._subvars)+')'

    def __repr__(self):
        return str(self)      
            
    def __getitem__(self, name):
        if self._subvars == None: return
        name = name_to_index(name)
        itemname = "%s[%s]" % (self._name, name)
        if name not in self._subvars:
            _var = var(self._prob, itemname) 
            self._subvars[name] = _var
        else:
            _var = self._subvars[name]
        return _var
        
    def __setitem__(self, name, value):
        if self._subvars == None: return
        name = name_to_index(name)
        itemname = "%s[%s]" % (self._name, name)
        new_var = var(self._prob, itemname) 
        self._subvars[name] = new_var
        new_var == value
        
    def __iter__(self):
        if self._subvars == None: return
        for x in self._subvars:
            yield x

class constraint(var):
    def __str__(self):
        if self._subvars == None:
            return '(constraint:'+str(self._value)+')'
        else:
            return '(constraint:'+str(self._subvars)+')'

class objective(var):
    def __str__(self):
        if self._subvars == None:
            return '(objective:'+str(self._value)+')'
        else:
            return '(objective:'+str(self._subvars)+')'
            
class nothing:
    def __repr__(self):
        return ''       
