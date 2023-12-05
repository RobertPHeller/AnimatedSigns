#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Dec 5 14:41:42 2023
#  Last Modified : <231205.1532>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
## @copyright
#    Copyright (C) 2023  Robert Heller D/B/A Deepwoods Software
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
# @file generateoutline.tcl
# @author Robert Heller
# @date Tue Dec 5 14:41:42 2023
# 
#
#*****************************************************************************


package require snit

snit::type GenerateOutline {
    typevariable Poly { {62 12} {90 18} {90 22} {102 22} {102 36} {94 36} 
        {94 69} {102 69} {102 81} {94 81} {94 243} {87 243} {87 81} {35 81} 
        {35 243} {27 243} {27 81} {21 81} {21 69} {27 69} {27 36} {20 36} 
        {20 22} {32 22} {32 18} {62 12} }
    typevariable pixelscale .3495412844
    typeconstructor {
        set file [from ::argv -outfile temp.pcb]
        set boardedgeX [from ::argv -bx 100]
        set boardedgeY [from ::argv -by 100]
        set fp [open $file w]
        set last {}
        foreach p $Poly {
            if {$last ne {}} {
                puts $fp [format {(gr_line (start %f %f) (end %f %f) (layer "Edge.Cuts") (width 0.1)  (tstamp 0de56762-ce56-43f6-b2d4-e1179688ff91))} \
                          [expr {([lindex $last 0] * $pixelscale) + $boardedgeX}] \
                          [expr {([lindex $last 1] * $pixelscale) + $boardedgeY}] \
                          [expr {([lindex $p 0] * $pixelscale) + $boardedgeX}] \
                          [expr {([lindex $p 1] * $pixelscale) + $boardedgeY}]]
            }
            set last $p
        }
        close $fp
    }
}

                
