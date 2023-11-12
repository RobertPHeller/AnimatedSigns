#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Sun Nov 12 12:33:36 2023
#  Last Modified : <231112.1408>
#
#  Description	
#
#  Notes
#
#  History
#	
#*****************************************************************************
#
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
#
# 
#
#*****************************************************************************


import Part
from FreeCAD import Base
import FreeCAD as App

from abc import ABCMeta, abstractmethod, abstractproperty
from math import *

class SixFootHood(object):
    __LightLength__ = 21.02
    __LightWidth__ = 1.7517
    __LightTermSpacing__ = 19.05
    __LightTermWireHoleRad = 0.5
    __HoodHeight__ = 3.5
    __HoodLength__ = 25
    def __init__(self,name,origin):
        self.name=name
        if not isinstance(origin,Base.Vector):
             raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        XNorm=Base.Vector(1.0,0,0)
        whole = Part.Face(Part.Wire(Part.makeCircle(self.__HoodHeight__,\
                                                    self.origin,\
                                                    XNorm)))\
                        .extrude(Base.Vector(self.__HoodLength__,0,0))
        whole = whole.cut(Part.makePlane(self.__HoodLength__,\
                                             self.__HoodHeight__*2,\
                                             self.origin.add(Base.Vector(0,-self.__HoodHeight__,0)))\
                                        .extrude(Base.Vector(0,0,self.__HoodHeight__)))
        interierRad = self.__HoodHeight__*.9
        interierLen = self.__HoodLength__-(self.__HoodHeight__*.1)
        interierXOff = (self.__HoodLength__-interierLen)/2.0 
        whole = whole.cut(Part.Face(Part.Wire(Part.makeCircle(interierRad,\
                                                              self.origin.add(Base.Vector(interierXOff,0,0)),\
                                                              XNorm)))\
                         .extrude(Base.Vector(interierLen,0,0)))
        hole1Xoff = (self.__HoodLength__-self.__LightTermSpacing__)/2.0
        h1orig = self.origin.add(Base.Vector(hole1Xoff,0,-self.__HoodHeight__))
        h2orig = h1orig.add(Base.Vector(self.__LightTermSpacing__,0,0))
        whole = whole.cut(Part.Face(Part.Wire(Part.makeCircle(self.__LightTermWireHoleRad,\
                                                              h1orig)))\
                                .extrude(Base.Vector(0,0,self.__HoodHeight__*.3)))
        whole = whole.cut(Part.Face(Part.Wire(Part.makeCircle(self.__LightTermWireHoleRad,\
                                                              h2orig)))\
                                .extrude(Base.Vector(0,0,self.__HoodHeight__*.3)))
        self.hood = whole
    def show(self,doc=None):
        if doc==None:
            doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.hood
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        


if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    hood = SixFootHood("Hood",Base.Vector(0,0,0))
    hood.show(doc)
    Gui.SendMsgToActiveView("ViewFit")
    
