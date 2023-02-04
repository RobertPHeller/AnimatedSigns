#*****************************************************************************
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Fri Feb 3 15:28:08 2023
#  Last Modified : <230203.1958>
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

class VCueFace(object):
    def __init__(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        end=Part.Face(Part.Wire(Part.makeCircle(1.0,Base.Vector(30,74,0))))
        stick=Part.Face(Part.Wire(Part.makePolygon([(29,74,0),(31,74,0),(30,5,0),(29,74,0)])))
        self.face=end.fuse(stick).translate(origin)
        
class ArrowFace(object):
    def __init__(self,origin,headlength=5.08,headthickness=5.08,\
                 thickness=2.54,tipy=2.54,tipx=10.16,\
                 taily=2.54,tailx=31):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        halfheadthickness = headthickness / 2.0
        #print("*** ArrowFace() halfheadthickness is ",halfheadthickness,file=sys.stderr)
        halfthichness = thickness/2.0
        #print("*** ArrowFace() halfthichness is ",halfthichness,file=sys.stderr)
        dx=tipx-tailx
        dy=tipy-taily
        #print("*** ArrowFace() dx,dy are ",dx,dy,file=sys.stderr)
        arrowlength= sqrt((dx*dx) + (dy*dy))
        #print("*** ArrowFace() arrowlength is ",arrowlength,file=sys.stderr)
        angleRads = atan2(dy,dx)
        angle = (angleRads/pi)*180
        #print("*** ArrowFace() angle is ",angle,file=sys.stderr)
        base = arrowlength-headlength
        #print("*** ArrowFace() base is ",base,file=sys.stderr)
        polypoints = list()
        polypoints.append(Base.Vector(0,halfthichness,0))
        polypoints.append(Base.Vector(base,halfthichness,0))
        polypoints.append(Base.Vector(base,halfheadthickness,0))
        polypoints.append(Base.Vector(arrowlength,0,0))
        polypoints.append(Base.Vector(base,-halfheadthickness,0))
        polypoints.append(Base.Vector(base,-halfthichness,0))
        polypoints.append(Base.Vector(0,-halfthichness,0))
        polypoints.append(Base.Vector(0,halfthichness,0))
        self.face=Part.Face(Part.Wire(Part.makePolygon(polypoints)))
        self.face=self.face.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),angle)
        self.face=self.face.translate(Base.Vector(tailx,taily,0))
        self.face=self.face.translate(origin)

class WholeSignPath(object):
    _wholeSignPoly = [(5.715,5.08,0),(5.715,22.86,0),(10.16,22.86,0),(10.16,76.2,0),\
                      (31.75,76.2,0),(31.75,0,0),(10.16,0,0),(10.16,5.08,0),\
                      (5.715,5.08,0)]
    def __init__(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        polypoints = list()
        for tup in self._wholeSignPoly:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        self.face=Part.Face(Part.Wire(Part.makePolygon(polypoints)))
        
class SignPCB(object):
    _pcbPoly = [(0,5.08,0),(0,22.86,0),(10.16,22.86,0),(10.16,76.2,0),\
                      (31.75,76.2,0),(31.75,0,0),(10.16,0,0),(10.16,5.08,0),\
                      (0,5.08,0)]
    def __init__(self,name,origin):
        self.name=name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        polypoints = list()
        for tup in self._pcbPoly:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        self.board=Part.Face(Part.Wire(Part.makePolygon(polypoints))).extrude(Base.Vector(0,0,1.5))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.board
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        
class Sign(object):
    def __init__(self,name,origin):
        self.name=name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.board = SignPCB(name+"_board",origin)
        signcaseface = WholeSignPath(origin.add(Base.Vector(0,0,1.5)))
        self.case = signcaseface.face.extrude(Base.Vector(0,0,5))
        arrowface = ArrowFace(origin.add(Base.Vector(0,0,6.5)))
        self.arrow = arrowface.face.extrude(Base.Vector(0,0,.1))
        cueface = VCueFace(origin.add(Base.Vector(0,0,6.5)))
        self.cue = cueface.face.extrude(Base.Vector(0,0,.1))
        self.table = Part.makePlane(18-6.35,71.12-6.35,origin.add(Base.Vector(10.16+3.175,5.08+3.175,6.5))).extrude(Base.Vector(0,0,.1))
        self.tableOutline = Part.makePlane(18,71.12,origin.add(Base.Vector(10.16,5.08,6.5))).extrude(Base.Vector(0,0,.1))
        self.eightball = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,6.5))))).extrude(Base.Vector(0,0,.2))
        temp = Part.Face(Part.makeWireString("8","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        self.eightball8 = temp.translate(origin.add(Base.Vector(19.16-2.5,68-3,6.5))).extrude(Base.Vector(0,0,.3))
        self.bball = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,6.5))))).extrude(Base.Vector(0,0,.2))
        temp = Part.Face(Part.makeWireString("B","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        self.bballB = temp.translate(origin.add(Base.Vector(19.16-2.5,59-3,6.5))).extrude(Base.Vector(0,0,.3))
        self.aball = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,50,6.5))))).extrude(Base.Vector(0,0,.2))
        temp = Part.Face(Part.makeWireString("A","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        self.aballA = temp.translate(origin.add(Base.Vector(19.16-2.5,50-3,6.5))).extrude(Base.Vector(0,0,.3))
        self.l1ball = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,41,6.5))))).extrude(Base.Vector(0,0,.2))
        temp = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        self.l1ballL = temp.translate(origin.add(Base.Vector(19.16-2.5,41-3,6.5))).extrude(Base.Vector(0,0,.3))
        self.l2ball = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,6.5))))).extrude(Base.Vector(0,0,.2))
        temp = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        self.l2ballL = temp.translate(origin.add(Base.Vector(19.16-2.5,32-3,6.5))).extrude(Base.Vector(0,0,.3))
        club = Part.makeWireString("CLUB","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",2.6,0.0)
        self.club = list()
        self.club.append(Part.Face(club[0]).translate(origin.add(Base.Vector(19.16-4,32-10,6.5))).extrude(Base.Vector(0,0,.2)))
        self.club.append(Part.Face(club[1]).translate(origin.add(Base.Vector(19.16-4,32-13,6.5))).extrude(Base.Vector(0,0,.2)))
        self.club.append(Part.Face(club[2]).translate(origin.add(Base.Vector(19.16-4,32-16,6.5))).extrude(Base.Vector(0,0,.2)))
        self.club.append(Part.Face(club[3]).translate(origin.add(Base.Vector(19.16-4,32-19,6.5))).extrude(Base.Vector(0,0,.2)))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_case")
        obj.Shape=self.case
        obj.Label=self.name+"_case"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_arrow")
        obj.Shape=self.arrow
        obj.Label=self.name+"_arrow"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_cue")
        obj.Shape=self.cue
        obj.Label=self.name+"_cue"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_table")
        obj.Shape=self.table
        obj.Label=self.name+"_table"
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_tableOutline")
        obj.Shape=self.tableOutline
        obj.Label=self.name+"_tableOutline"
        obj.ViewObject.ShapeColor=tuple([0.647,0.1647,0.1647])
        obj = doc.addObject("Part::Feature",self.name+"_eightball")
        obj.Shape=self.eightball
        obj.Label=self.name+"_eightball"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_eightball8")
        obj.Shape=self.eightball8
        obj.Label=self.name+"_eightball8"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_bball")
        obj.Shape=self.bball
        obj.Label=self.name+"_bball"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_bballB")
        obj.Shape=self.bballB
        obj.Label=self.name+"_bballB"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_aball")
        obj.Shape=self.aball
        obj.Label=self.name+"_aball"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_aballA")
        obj.Shape=self.aballA
        obj.Label=self.name+"_aballA"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ball")
        obj.Shape=self.l1ball
        obj.Label=self.name+"_l1ball"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ballL")
        obj.Shape=self.l1ballL
        obj.Label=self.name+"_l1ballL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ball")
        obj.Shape=self.l2ball
        obj.Label=self.name+"_l2ball"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ballL")
        obj.Shape=self.l2ballL
        obj.Label=self.name+"_l2ballL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubC")
        obj.Shape=self.club[0]
        obj.Label=self.name+"_clubC"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubL")
        obj.Shape=self.club[1]
        obj.Label=self.name+"_clubL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubU")
        obj.Shape=self.club[2]
        obj.Label=self.name+"_clubU"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubB")
        obj.Shape=self.club[3]
        obj.Label=self.name+"_clubB"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        
        self.board.show()

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    sign = Sign("pcb",Base.Vector(0,0,0))
    sign.show()
    Gui.SendMsgToActiveView("ViewFit")
