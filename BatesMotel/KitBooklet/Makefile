##-*- makefile -*-############################################################
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon May 13 10:49:19 2024
#  Last Modified : <240514.0902>
#
#  Description	
#
#  Notes
#
#  History
#	
#  $Log$
#
##############################################################################
#
#    Copyright (C) 2024  Robert Heller D/B/A Deepwoods Software
#			51 Locke Hill Road
#			Wendell, MA 01379-9728
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# 
#
##############################################################################


SRCS = KitBooklet.tex BatesMotelBackPCB.png BatesMotelFrontPCB.png


all: KitBooklet-book.pdf

KitBooklet-book.pdf: KitBooklet.pdf
	pdfbook2 KitBooklet.pdf
	

KitBooklet.pdf: $(SRCS)
	-rm *.aux *.toc *.out *.log
	pdflatex KitBooklet.tex
	pdflatex KitBooklet.tex
	pdflatex KitBooklet.tex
	pdflatex KitBooklet.tex
	
