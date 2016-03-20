/* *** This is C code *** 
   Filename : glpk.i (primitives for swig producing the python-glpk API)
*/

/*----------------------------------------------------------------------
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
----------------------------------------------------------------------*/

%module glpkpi
%{
#include "./glpk.h"
%}

/* Some global variable declarations */

/* Some read-only variables */
%immutable;

/* Some more variables */
%mutable;

/* Functions for creating C arrays in Python; see usage in 'example_refman.py' */
%include "carrays.i"
%array_class(int, intArray);
/* a = intArray(SIZE) -> "a" can be passed to C functions as int *, int [], ... */
%array_class(double, doubleArray);
/* a = doubleArray(SIZE) -> "a" can be passed to C functions as double *, double [], ... */

%include glpkpi.h
%include "./glpk.h"	/* change if glpk.h is installed somewhere else */
