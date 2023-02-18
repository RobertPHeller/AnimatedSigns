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
#  Last Modified : <230218.1642>
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
    @staticmethod
    def Width():
        return BarPoolTable.width_
    length_ = (78.0/87.0)*25.4
    @staticmethod
    def Length():
        return BarPoolTable.length_
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
        
class PoolTableLight(object):
    width_ = (18.0/87.0)*25.4
    @staticmethod
    def Width():
        return PoolTableLight.width_
    length_ = (72.0/87.0)*25.4
    @staticmethod
    def Length():
        return PoolTableLight.length_
    flatwidth_ = (6.0/87.0)*25.4
    @staticmethod
    def FlatWidth():
        return PoolTableLight.flatwidth_
    curverad_ = (6.0/87.0)*25.4
    def __init__(self,name,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        XOrient = Base.Vector(1,0,0)
        lextrude = Base.Vector(self.length_,0,0)
        r = self.curverad_
        print("*** PoolTableLight(): origin is ",origin.x,origin.y,origin.z,file=sys.stderr)
        o = origin.add(Base.Vector(0,(self.flatwidth_/2.0+self.curverad_),-self.curverad_))
        print("*** PoolTableLight(): o [l] is ",o.x,o.y,o.z,file=sys.stderr)        
        a1c = Part.makeCircle(r,o,XOrient)
        a1 = Part.Face(Part.Wire(a1c)).extrude(lextrude)
        a2c = Part.makeCircle(r-.25,o,XOrient)
        a2 = Part.Face(Part.Wire(a2c)).extrude(lextrude)
        a1 = a1.cut(a2)
        b1w = self.curverad_
        b1l = self.curverad_*2
        b1orig = o.add(Base.Vector(0,0,-r))
        b1 = Part.makePlane(b1l,b1w,b1orig,XOrient).extrude(lextrude)
        al = a1.cut(b1)
        b1orig = b1orig.add(Base.Vector(0,r,0))
        b1 = Part.makePlane(b1w,b1w,b1orig,XOrient).extrude(lextrude)
        al = al.cut(b1)
        o = origin.add(Base.Vector(0,(self.flatwidth_/2.0),0))
        f = Part.makePlane(self.length_,self.flatwidth_,o).extrude(Base.Vector(0,0,-.25))
        o = origin.add(Base.Vector(0,-(self.flatwidth_/2.0-self.curverad_),-self.curverad_))
        print("*** PoolTableLight(): o [r] is ",o.x,o.y,o.z,file=sys.stderr)        
        a1c = Part.makeCircle(r,o,XOrient)
        a1 = Part.Face(Part.Wire(a1c)).extrude(lextrude)
        a2c = Part.makeCircle(r-.25,o,XOrient)
        a2 = Part.Face(Part.Wire(a2c)).extrude(lextrude)
        ar = a1.cut(a2)
        b1w = self.curverad_
        b1l = self.curverad_*2
        b1orig = o.add(Base.Vector(0,r,-r))
        b1 = Part.makePlane(b1l,b1w,b1orig,XOrient).extrude(lextrude)
        ar = ar.cut(b1)
        b1orig = b1orig.add(Base.Vector(0,0,0))
        b1 = Part.makePlane(b1w,b1l,b1orig,XOrient).extrude(lextrude)
        ar = ar.cut(b1)
        self.a = al.fuse(f).fuse(ar)
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.a
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
    
class Booth(object):
    length_ = (48.0/87.0)*25.4
    width_  = (24.0/87.0)*25.4
    height_ = (42.0/87.0)*25.4
    @staticmethod
    def Spacing():
        return (66.0/87.0)*25.4
    @staticmethod
    def Length():
        return Booth.length_
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
    @staticmethod
    def Depth():
        return Hall.depth_
    width_ = (5.0+13.0/16.0)*25.4
    @staticmethod
    def Width():
        return Hall.width_
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
        
class Wall(object):
    thick_ = (3.0/87)*25.4
    height_ = ((8.0*12)/87)*25.4
    def __init__(self,name,origin,length,ishoriz=True):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        if ishoriz:
            self.wall = Part.makePlane(length,self.thick_,origin).extrude(Base.Vector(0,0,self.height_))
        else:
            self.wall = Part.makePlane(self.thick_,length,origin).extrude(Base.Vector(0,0,self.height_))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.wall
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])

class Door(object):
    thick_ = (3.0/87)*25.4
    height_ = ((7.0*12)/87)*25.4
    width_ = (25.0/87)*25.4
    @staticmethod
    def Width():
        return Door.width_
    def __init__(self,name,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        self.door = Part.makePlane(self.width_,self.thick_,origin).extrude(Base.Vector(0,0,self.height_))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.door
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([165.0/255.0,42.0/255.0,42.0/255.0])
        
class Bar(object):
    width_ = (24.0/87)*25.4
    height_ = (42.0/87)*25.4
    def __init__(self,name,origin,length):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.name = name
        self.bar = Part.makePlane(self.width_,length,origin).extrude(Base.Vector(0,0,self.height_))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.bar
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([165.0/255.0,42.0/255.0,42.0/255.0])
    
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
    backwall = Wall("backwall",b1.origin.add(Base.Vector(0,Booth.Length(),0)),Hall.Width())
    backwall.show()
    gents = Door("gents",b4.origin.add(Base.Vector((6/87)*25.4,Booth.Length(),0)))
    gents.show()
    backdepth = Hall.Depth() - (backwall.origin.y-floor.origin.y)
    rrwall1 = Wall("restroomwall1",gents.origin.add(Base.Vector(Door.Width()+((6-1.5)/87)*25.4,0,0)),backdepth,False)
    rrwall1.show()
    rrwall2Xoff = rrwall1.origin.x-floor.origin.x
    rrwall2 = Wall("restroomwall2",rrwall1.origin.add(Base.Vector(rrwall2Xoff,0,0)),backdepth,False)
    rrwall2.show()
    ladies = Door("ladies",gents.origin.add(Base.Vector(Door.Width()+(12/87)*25.4,0,0)))
    ladies.show()
    b5 = Booth("booth5",ladies.origin.add(Base.Vector(Door.Width()+(6/87)*25.4,-Booth.Length(),0)))
    b5.show()
    b6 = Booth("booth6",b5.origin.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b6.show()
    b7 = Booth("booth7",b5.origin.add(Base.Vector(Booth.Spacing(),0,0)))
    b7.show()
    b8 = Booth("booth8",b7.origin.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b8.show()
    b9 = Booth("booth9",b7.origin.add(Base.Vector(Booth.Spacing(),0,0)))
    b9.show()
    b10 = Booth("booth10",b9.origin.add(Base.Vector(Booth.Spacing(),0,0)),False)
    b10.show()
    bardoor = Door("bardoor",backwall.origin.add(Base.Vector(Hall.Width()-(6/87)*25.4-Door.Width(),0,0)))
    bardoor.show()
    barX = b10.origin.x+((30.0/87)*25.4)
    barorig = floor.origin.add(Base.Vector(barX,0,1))
    barlen = backwall.origin.y-floor.origin.y
    bar = Bar("bar",barorig,barlen)
    bar.show()
    l1x = t1.origin.x+(BarPoolTable.Length()-PoolTableLight.Length())/2.0
    lz = floor.origin.z+(72.0/87)*25.4
    l1y = t1.origin.y+(BarPoolTable.Width()/2.0)-(PoolTableLight.FlatWidth())
    l = PoolTableLight("pooltablelight",Base.Vector(l1x,
                                                    l1y,\
                                                    lz))
    l.show()
    Gui.activeDocument().activeView().viewLeft()
    Gui.SendMsgToActiveView("ViewFit")
    

    
