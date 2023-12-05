#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Tue Dec 5 13:25:36 2023
#  Last Modified : <231205.1438>
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
# @file getoutline.tcl
# @author Robert Heller
# @date Tue Dec 5 13:25:36 2023
# 
#
#*****************************************************************************


package require snit
package require Img

snit::type MakePCBOutline {
    typeconstructor {
        set file [from ::argv -bitmap {}]
        if {$file eq {}} {
            puts stderr "$::argv0: -bitmap is required!"
            exit 99
        }
        set bitmap [image create photo -file $file]
        set width [image width $bitmap]
        set height [image height $bitmap]
        puts stderr "*** [$bitmap cget -file]: ${width}x${height}"
        set boardedgeX [from ::argv -bx 100]
        set boardedgeY [from ::argv -by 100]
        set pen up
        for {set y 0} {$y < $height} {incr y} {
            for {set x 0} {$x < $width} {incr x} {
                set bit [lindex [$bitmap get $x $y] 0]
                if {$bit == 0} {
                    puts stderr "*** black at $x,$y"
                }
            }
        }
        
    }
}

exit
