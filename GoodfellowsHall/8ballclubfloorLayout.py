#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri Feb 17 15:01:16 2023
#  Last Modified : <230217.1554>
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

class BarPoolTable(object):
    width_ = (39.0/87.0)*25.4
    length_ = (78.0/87.0)*25.4
    height_ = (30.0/87.0)*25.4
    @staticmethod
    def Spacing():
        return (60.0/87.0)*25.4
    def NextTableX(self):
        return self.origin.add(Base.Vector(self.length_+BarPoolTable.Spacing(),0,0))
    def NextTableY(self):
        return self.origin.add(Base.Vector(0,self.width_+BarPoolTable.Spacing(),0))
    def __init__(self,name,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        self.table = Part.makePlane(self.length_,self.width_,origin).extrude(Base.Vector(0,0,self.height_))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.table
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        
class Booth(object):
    length_ = (48.0/87.0)*25.4
    width_  = (24.0/87.0)*25.4
    height_ = (42.0/87.0)*25.4
    @staticmethod
    def Spacing():
        return (66.0/87.0)*25.4
    def __init__(self,name,origin,left=True):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        if left:
            self.booth = Part.makePlane(self.width_,self.length_,origin).extrude(Base.Vector(0,0,self.height_))
        else:
            self.booth = Part.makePlane(self.width_,self.length_,origin.add(Base.Vector(-self.width_,0,0))).extrude(Base.Vector(0,0,self.height_))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.booth
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        
class Hall(object):
    depth_ = (4.0+5.0/8.0)*25.4
    width_ = (5.0+13.0/16.0)*25.4
    def __init__(self,name,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        self.floor = Part.makePlane(self.width_,self.depth_,origin).extrude(Base.Vector(0,0,1))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.floor
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    floor = Hall("floor",Base.Vector(0,0,0))
    floor.show()
    t1orig = floor.origin.add(Base.Vector(BarPoolTable.Spacing(),BarPoolTable.Spacing(),1))
    t1 = BarPoolTable("table1",t1orig);
    t1.show()
    t2 = BarPoolTable("table2",t1.NextTableX())
    t2.show()
    t3 = BarPoolTable("table3",t1.NextTableY())
    t3.show()
    t4 = BarPoolTable("table4",t2.NextTableY())
    t4.show()
    boothstart = t3.NextTableY()
    boothorig = Base.Vector(floor.origin.x,boothstart.y,boothstart.z)
    b1 = Booth("booth1",boothorig)
    b1.show()
    b2 = Booth("booth2",boothorig.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b2.show()
    b3 = Booth("booth3",b2.origin)
    b3.show()
    b4 = Booth("booth4",b2.origin.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b4.show()
    b5 = Booth("booth5",b4.origin.add(Base.Vector(Booth.Spacing(),0,0)))
    b5.show()
    b6 = Booth("booth6",b5.origin.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b6.show()
    Gui.SendMsgToActiveView("ViewFit")
    

    
