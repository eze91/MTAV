"""
   Filename:  glpk.py (define a class for calling GLPK from Python)

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
from model_objects import *
from glpk_parser import *
from glpkpi import *
from array import *
import sys
import os
import tempfile
LOG = False
VERBOSE = False
DEBUG = False

GLPK_VERSION = glp_version();

class glpk:
    def __init__(self, mod_file = None, dat_file = None):
        ### # parameter structure:    NOT USED YET
        self._parm = glp_smcp();
        glp_init_smcp(self._parm);
        #self._parm.msg_lev = GLP_MSG_OFF;    # silent modes
        #self._parm.msg_lev = GLP_MSG_ALL;
        self._parm.msg_lev = GLP_MSG_ERR;
        #self._parm.meth = GLP_DUAL;
        self._parm.meth = GLP_DUALP;
        #self._parm.meth = GLP_PRIMAL;
        
        self._tran = None
        self._lp = None
        self._type = {}
        self._model = ""
        self._ptype = None
        self._bounds = {}
        self._ready = False

        if mod_file == None:
            if VERBOSE:
                print "creating problem -- no file associated"
            self._lp = glp_create_prob();
        elif mod_file.find(".mps") != -1:
            if VERBOSE:
                print "creating problem from mps file"
            self._ptype = "mps"
            self._lp = glp_create_prob();
            ret = glp_read_mps(self._lp, GLP_MPS_FILE, None, mod_file);# !self._parm
            if ret != 0:
                print "Error reading model", mod_file
                raise IOError
            self._read_variables()
        elif mod_file.find(".lp") != -1:
            if VERBOSE:
                print "creating problem from lp file"
            self._ptype = "lp"
            self._lp = glp_create_prob();
            ret = glp_read_lp(self._lp, None, mod_file);# !self._parm
            self._read_variables()
        elif mod_file.find(".mod") != -1:
            if VERBOSE:
                print "creating problem from mod file"
            self._ptype = "mod"
            t = mod_file.rfind('.')
            if t<0: name = mod_file
            else: name = mod_file[:t]
            f, tmp_file = tempfile.mkstemp()
            
            # genereate a temporary model file
            parser = glpk_parser(mod_file, dat_file)
            parser.generate_model(tmp_file)
            if VERBOSE:
                print "temporary model file '%s' created" % (tmp_file)
            
            # read model           
            mod_file = tmp_file
            self._lp = glp_create_prob();
            self._tran = glp_mpl_alloc_wksp();
            ret = glp_mpl_read_model(self._tran, mod_file, 0);
            if ret != 0:
                print "Error reading model", mod_file
                raise IOError
            
            # load data        
            #glp_term_out(GLP_OFF);    
            f, output = tempfile.mkstemp()
            os.close(f)
            ret = glp_mpl_generate(self._tran, output)
            if ret != 0:
                print "Error generating model"
                raise IOError
            load_data(parser, output, self)
            if not DEBUG:
                os.remove(output)
                os.remove(tmp_file)
            #glp_term_out(GLP_ON);
            self._cols = self._rows = None
     
    def _delete(self):
        if self._tran and glp_mpl_free_wksp:
            glp_mpl_free_wksp(self._tran);
        if self._lp and glp_delete_prob:
            glp_delete_prob(self._lp);
      
    def _reload(self):
        if self._ptype != 'mod': return
        self._delete()
        # read model
        s = self._dump()
        f, mod_file = tempfile.mkstemp()
        os.write(f, s)
        os.close(f)
        self._lp = glp_create_prob();
        self._tran = glp_mpl_alloc_wksp();        
        ret = glp_mpl_read_model(self._tran, mod_file, 0);
        if ret != 0:
            print "Error reading model", mod_file
            raise IOError        
        #if not VERBOSE: glp_term_out(GLP_OFF);            
        ret = glp_mpl_generate(self._tran, None);
        if ret != 0:
            print "Error generating model"
            raise IOError
        glp_mpl_build_prob(self._tran, self._lp);
        #if not VERBOSE: glp_term_out(GLP_ON);
        if not DEBUG:
            os.remove(mod_file)
        
    def _dump(self):
        if self._ptype != 'mod': return
        s = self._model+"\ndata;\n"       
        for name in self._sets_names:
            if type(self[name])!=dict:
                val = str(self[name]).strip('[]')
                s += "set %s := %s;\n" % (name,val)    
            else:
                for subname in sorted(self[name]):
                    if type(subname)==str: 
                        sname = '\''+subname+'\''
                    elif type(subname)!=tuple:
                        sname = str(subname)
                    else:
                        sname = str(subname).strip('()')
                    val = str(self[name][subname]).strip('[]')
                    s += "set %s[%s] := %s;\n" % (name,sname,val)
        for name in self._params_names:
            if type(self[name])!=dict:
                if name not in self._default or self[name] != None:
                    s += "param %s := %s;\n" % (name,self[name])
                else:
                    val = self[name]
                    if val==None: val = ""
                    s += "param %s default %s := %s;\n" % (name,self._default[name],val)
            else:
                if name not in self._default:
                    s += "param %s :=" % (name)
                else:
                    s += "param %s default %s :=" % (name,self._default[name])
                for subname in sorted(self[name]):
                    if type(subname)==str: 
                        sname = '\''+subname+'\''
                    elif type(subname)!=tuple:
                        sname = str(subname)
                    else:
                        sname = str(subname).strip('()')
                    s += " [%s] %s" % (sname,self[name][subname]) 
                s += ";\n"                
        s += "end;\n"
        return s
 
    def _get_col_bnds(self, i):
        lb = glp_get_col_lb(self._lp, i);
        ub = glp_get_col_ub(self._lp, i);
        tp = glp_get_col_type(self._lp, i);
        bnds = (None, None)            
        if tp == GLP_LO:
            bnds = (('>=',lb),None)
        elif tp == GLP_UP:
            bnds = (None,('<=',ub))
        elif tp == GLP_DB:
            bnds =(('>=',lb),('<=',ub))
        elif tp == GLP_FX:
            bnds = ('=',lb)
        return bnds
        
    def _get_row_bnds(self, i):
        lb = glp_get_row_lb(self._lp, i);
        ub = glp_get_row_ub(self._lp, i);
        tp = glp_get_row_type(self._lp, i);
        bnds = (None, None)            
        if tp == GLP_LO:
            bnds = (('>=',lb),None)
        elif tp == GLP_UP:
            bnds = (None,('<=',ub))
        elif tp == GLP_DB:
            bnds =(('>=',lb),('<=',ub))
        elif tp == GLP_FX:
            bnds = ('=',lb)
        return bnds
        
    def _get_bounds(self, name):
        rows = self._rows
        cols = self._cols
        if name in rows:
            p = rows[name]
            if len(p)!=1:
                return None    
            return self._get_row_bnds(p[0])
        elif name in cols:
            p = cols[name]
            if len(p)!=1:
                return None            
            return self._get_col_bnds(p[0])
        else:
            return None
        
    def _read_variables(self):
        bounds = self._default_bounds = {}  
        
        cols = self._cols = {} 
        for i in xrange(1,glp_get_num_cols(self._lp)+1):
            name = glp_get_col_name(self._lp, i)
            tname = name[:max(0,name.find('['))]         
            bounds[name] = self._get_col_bnds(i)
            cols[name] = [i]
            if tname != "":
                if tname not in self._cols:
                    cols[tname] = [i]
                else:
                    cols[tname].append(i)
                    
        rows = self._rows = {}
        for i in xrange(1,glp_get_num_rows(self._lp)+1):
            name = glp_get_row_name(self._lp, i)
            tname = name[:max(0,name.find('['))]
            bounds[name] = self._get_row_bnds(i)
            rows[name] = [i]
            if tname != "":
                if tname not in self._cols:
                    rows[tname] = [i]
                else:
                    rows[tname].append(i)
        
    def _apply_bounds(self):
        rows = self._rows
        cols = self._cols
        types = {
            (None,None): GLP_FR,
            ('>=',None): GLP_LO,
            (None,'<='): GLP_UP,
            ('>=','<='): GLP_DB,
            ('='): GLP_FX
        }
        
        def conv(bnds):
            if bnds[0] == '=':
                return GLP_FX, bnds[1], bnds[1]
            else:
                l, lb = bnds[0], None
                if l != None: l,lb = l                  
                u, ub = bnds[1], None
                if u != None: u, ub = u
                if lb == None: lb = 0.0
                if ub == None: ub = 0.0
                return types[l,u], lb, ub
                
        for name in sorted(self._bounds):
            bnds = self._bounds[name]
            if len(bnds)==2 and name in self._default_bounds:
                dbnds = self._default_bounds[name]
                if dbnds[0]!='=':
                    if bnds[0]==None:
                        bnds = dbnds[0], bnds[1]
                    if bnds[1]==None:
                        bnds = bnds[0], dbnds[1]
            tp, lb, ub = conv(bnds)
            if name in cols:
                for i in cols[name]:
                    glp_set_col_bnds(self._lp, i, tp, lb, ub);
            elif name in rows:
                for i in rows[name]:
                    glp_set_row_bnds(self._lp, i, tp, lb, ub);
            else:
                print 'model object not found!'
        
    def _set_bounds(self, varname,(_type,_value)):
        dic = self._bounds
        if varname in dic:
            bnds = dic[varname]
            if bnds[0] == '=':
                bnds = (None, None)
        else:
            bnds = dic[varname] = (None, None)
        if _type == '=':
            bnds = ('=', _value)
        elif _type == '<=':
            bnds = (bnds[0], (_type,_value))
        elif _type == '>=':
            bnds = ((_type,_value), bnds[1])        
        dic[varname] = bnds
        
    def _rm_bounds(self, varname):
        dic = self._bounds
        if varname in dic:
            del dic[varname]

    def _instantiate_solution(self):
        sol = {}
        name = glp_get_obj_name(self._lp)
        if glp_get_num_int(self._lp) == 0:  # problem is continuous
            value = glp_get_obj_val(self._lp)
            sol[name] = value
            for i in xrange(1,glp_get_num_cols(self._lp)+1):
                name = glp_get_col_name(self._lp, i)
                value = glp_get_col_prim(self._lp, i)
                sol[name] = value
        else:   # problem is MIP
            value = glp_mip_obj_val(self._lp)
            sol[name] = value
            for i in xrange(1,glp_get_num_cols(self._lp)+1):
                name = glp_get_col_name(self._lp, i)
                if glp_get_col_kind(self._lp, i) == GLP_CV:
                    value = glp_mip_col_val(self._lp, i)
                elif glp_get_col_kind(self._lp, i) in [GLP_IV, GLP_BV]:
                    # to avoid finite precision problems:
                    value = int(round(glp_mip_col_val(self._lp, i),0))
                else:
                    print "unkown col kind"
                    raise AttributeError
                sol[name] = value             
        self._sol = sol
        load_solution(sol, self)        
        
    def __del__(self):
        print "deleting glpk object"
        self._delete()         
        
    def __getitem__(self, name):
        return self.__dict__[name]
        
    def __setitem__(self, name, value):
        self.__dict__[name] = value
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value
     
    def __iter__(self):
        for name in self.__dict__:
            if name in self._type:
                yield name

    # interface
    def update(self):
        self._dump()
        self._reload()
        self._ready = True

    def solution(self):
        try:
            return self._sol
        except:
            return None

    def sets(self):
        try:
            return self._sets_names
        except:
            return None    

    def parameters(self):
        try:
            return self._params_names
        except:
            return None  

    def variables(self):
        try:
            return self._vars_names
        except:
            return None

    def constraints(self):
        try:
           return self._constraints_names
        except:
            return None 

    def objectives(self):
        try:
           return self._objectives_names
        except:
            return None

    def typeof(self, obj):
        try:
            return self._type[obj]
        except:
            return None

    def solve(self, instantiate = True, bounds = True):
        #glp_term_out(GLP_OFF);
        if not self._ready:
            self.update()
        #glp_term_out(GLP_ON);
        if self._cols == None or self._rows == None:
            self._read_variables()
        if bounds:
            self._apply_bounds()
        if glp_get_num_int(self._lp) == 0:   # problem is continuous
            res = glp_simplex(self._lp, self._parm) # self._parm !!!
        else:   # problem is MIP
            if self._tran:
                glp_mpl_build_prob(self._tran, self._lp);
            res = glp_simplex(self._lp, self._parm);  # ??? should use dual simplex ???
            glp_intopt(self._lp, None);
            if self._tran:
                ret = glp_mpl_postsolve(self._tran, self._lp, GLP_MIP);
                if ret != 0:
                    print "Error on postsolving model"
                    raise AttributeError
        if instantiate:
            self._instantiate_solution()     
        if res != 0:
            return None
        else:
            return glp_get_obj_val(self._lp);        

