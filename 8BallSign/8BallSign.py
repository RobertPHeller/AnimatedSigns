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
#  Last Modified : <230215.1514>
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
    def CueCutout(self,Z,depth):
        orig = Base.Vector(self.origin.x+29,self.origin.y+5,Z)
        return Part.makePlane(2,73-5,orig).extrude(Base.Vector(0,0,depth))
        
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
    _wholeSignPoly = [(5.715,5.08,0),(5.715,29.21,0),(10.16,29.21,0),(10.16,76.2,0),\
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
    _pcbPoly = [(0,5.08,0),(0,29.21,0),(10.16,29.21,0),(10.16,76.2,0),\
                      (31.75,76.2,0),(31.75,0,0),(10.16,0,0),(10.16,5.08,0),\
                      (0,5.08,0)]
    def __init__(self,name,origin,extrude=1):
        self.name=name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        polypoints = list()
        for tup in self._pcbPoly:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        self.board=Part.Face(Part.Wire(Part.makePolygon(polypoints))).extrude(Base.Vector(0,0,1.5*extrude))
        self.polypoints = polypoints
        self.surfaceZ = origin.z+(1.5*extrude)
        self.extrude = extrude
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name)
        obj.Shape=self.board
        obj.Label=self.name
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        
class SignBothSides(object):
    def __init__(self,name,origin):
        self.name=name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.boardL = SignPCB(name+"_pcbL",origin)
        self.boardR = SignPCB(name+"_pcbR",origin,-1)
        signcaseface = WholeSignPath(origin.add(Base.Vector(0,0,1.5)))
        self.caseL = signcaseface.face.extrude(Base.Vector(0,0,2))
        signcaseface = WholeSignPath(origin.add(Base.Vector(0,0,-1.5)))
        self.caseR = signcaseface.face.extrude(Base.Vector(0,0,-2))
        arrowface = ArrowFace(origin.add(Base.Vector(0,0,3.5)))
        self.arrowL = arrowface.face.extrude(Base.Vector(0,0,.1))
        arrowcut = ArrowFace(origin.add(Base.Vector(0,0,1.5))).face.extrude(Base.Vector(0,0,2))
        self.caseL = self.caseL.cut(arrowcut)
        arrowface = ArrowFace(origin.add(Base.Vector(0,0,-3.5)))
        self.arrowR = arrowface.face.extrude(Base.Vector(0,0,-.1))
        arrowcut = ArrowFace(origin.add(Base.Vector(0,0,-1.5))).face.extrude(Base.Vector(0,0,-2))
        self.caseR = self.caseR.cut(arrowcut)
        cueface = VCueFace(origin.add(Base.Vector(0,0,3.5)))
        self.cueL = cueface.face.extrude(Base.Vector(0,0,.1))
        self.caseL = self.caseL.cut(cueface.CueCutout(1.5,2))
        cueface = VCueFace(origin.add(Base.Vector(0,0,-3.5)))
        self.cueR = cueface.face.extrude(Base.Vector(0,0,-.1))
        self.caseR = self.caseR.cut(cueface.CueCutout(-1.5,-2))
        self.tableL = Part.makePlane(18-6.35,71.12-6.35,origin.add(Base.Vector(10.16+3.175,5.08+3.175,3.5))).extrude(Base.Vector(0,0,.1))
        self.tableR = Part.makePlane(18-6.35,71.12-6.35,origin.add(Base.Vector(10.16+3.175,5.08+3.175,-3.5))).extrude(Base.Vector(0,0,-.1))
        self.tableOutlineL = Part.makePlane(18,71.12,origin.add(Base.Vector(10.16,5.08,3.5))).extrude(Base.Vector(0,0,.1))
        self.tableOutlineR = Part.makePlane(18,71.12,origin.add(Base.Vector(10.16,5.08,-3.5))).extrude(Base.Vector(0,0,-.1))
        self.eightballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,3.5))))).extrude(Base.Vector(0,0,.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,1.5))))).extrude(Base.Vector(0,0,2)))
        self.eightballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,-3.5))))).extrude(Base.Vector(0,0,-.2))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,-1.5))))).extrude(Base.Vector(0,0,-2)))
        tempL = Part.Face(Part.makeWireString("8","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy()
        self.eightball8L = tempL.translate(origin.add(Base.Vector(19.16-2.5,68-3,3.5))).extrude(Base.Vector(0,0,.3))
        self.eightball8R = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,68-3,-3.5))).extrude(Base.Vector(0,0,-.3))
        self.bballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,3.5))))).extrude(Base.Vector(0,0,.2))
        self.bballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,-3.5))))).extrude(Base.Vector(0,0,-.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,1.5))))).extrude(Base.Vector(0,0,2)))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,-1.5))))).extrude(Base.Vector(0,0,-2)))
        tempL = Part.Face(Part.makeWireString("B","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.bballBL = tempL.translate(origin.add(Base.Vector(19.16-2.5,59-3,3.5))).extrude(Base.Vector(0,0,.3))
        self.bballBR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,59-3,-3.5))).extrude(Base.Vector(0,0,-.3))
        self.aballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,50,3.5))))).extrude(Base.Vector(0,0,.2))
        self.aballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,50,-3.5))))).extrude(Base.Vector(0,0,-.2))
        tempL = Part.Face(Part.makeWireString("A","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy()
        self.aballAL = tempL.translate(origin.add(Base.Vector(19.16-2.5,50-3,3.5))).extrude(Base.Vector(0,0,.3))
        self.aballAR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,50-3,-3.5))).extrude(Base.Vector(0,0,-.3))
        self.l1ballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,41,3.5))))).extrude(Base.Vector(0,0,.2))
        self.l1ballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,41,-3.5))))).extrude(Base.Vector(0,0,-.2))
        tempL = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.l1ballLL = tempL.translate(origin.add(Base.Vector(19.16-2.5,41-3,3.5))).extrude(Base.Vector(0,0,.3))
        self.l1ballLR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,41-3,-3.5))).extrude(Base.Vector(0,0,-.3))
        self.l2ballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,3.5))))).extrude(Base.Vector(0,0,.2))
        self.l2ballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,-3.5))))).extrude(Base.Vector(0,0,-.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,1.5))))).extrude(Base.Vector(0,0,2)))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,-1.5))))).extrude(Base.Vector(0,0,-2)))
        self.caseL = self.caseL.cut(Part.makePlane(4.572*2,59-32,origin.add(Base.Vector(19.16-4.572,32,1.5))).extrude(Base.Vector(0,0,2)))
        self.caseR = self.caseR.cut(Part.makePlane(4.572*2,59-32,origin.add(Base.Vector(19.16-4.572,32,-1.5))).extrude(Base.Vector(0,0,-2)))
        tempL = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.l2ballLL = tempL.translate(origin.add(Base.Vector(19.16-2.5,32-3,3.5))).extrude(Base.Vector(0,0,.3))
        self.l2ballLR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,32-3,-3.5))).extrude(Base.Vector(0,0,-.3))
        club = Part.makeWireString("CLUB","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",2.6,0.0)
        self.clubL = list()
        self.clubR = list()
        self.clubL.append(Part.Face(club[0]).translate(origin.add(Base.Vector(19.16-4,32-10,3.5))).extrude(Base.Vector(0,0,.2)))
        self.clubL.append(Part.Face(club[1]).translate(origin.add(Base.Vector(19.16-4,32-13,3.5))).extrude(Base.Vector(0,0,.2)))
        self.clubL.append(Part.Face(club[2]).translate(origin.add(Base.Vector(19.16-4,32-16,3.5))).extrude(Base.Vector(0,0,.2)))
        self.clubL.append(Part.Face(club[3]).translate(origin.add(Base.Vector(19.16-4,32-19,3.5))).extrude(Base.Vector(0,0,.2)))
        self.clubR.append(Part.Face(club[0]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-10,-3.5))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[1]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-13,-3.5))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[2]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-16,-3.5))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[3]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-19,-3.5))).extrude(Base.Vector(0,0,-.2)))
        self.caseL = self.caseL.cut(Part.makePlane(10,14,origin.add(Base.Vector(14,11,1.5))).extrude(Base.Vector(0,0,2)))
        self.caseR = self.caseR.cut(Part.makePlane(10,14,origin.add(Base.Vector(14,11,-1.5))).extrude(Base.Vector(0,0,-2)))
    def show(self):
        doc = App.activeDocument()
        obj = doc.addObject("Part::Feature",self.name+"_caseL")
        obj.Shape=self.caseL
        obj.Label=self.name+"_caseL"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_caseR")
        obj.Shape=self.caseR
        obj.Label=self.name+"_caseR"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_arrowL")
        obj.Shape=self.arrowL
        obj.Label=self.name+"_arrowL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_arrowR")
        obj.Shape=self.arrowR
        obj.Label=self.name+"_arrowR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_cueL")
        obj.Shape=self.cueL
        obj.Label=self.name+"_cueL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_cueR")
        obj.Shape=self.cueR
        obj.Label=self.name+"_cueR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_tableL")
        obj.Shape=self.tableL
        obj.Label=self.name+"_tableL"
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_tableR")
        obj.Shape=self.tableR
        obj.Label=self.name+"_tableR"
        obj.ViewObject.ShapeColor=tuple([0.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_tableOutlineL")
        obj.Shape=self.tableOutlineL
        obj.Label=self.name+"_tableOutlineL"
        obj.ViewObject.ShapeColor=tuple([0.647,0.1647,0.1647])
        obj = doc.addObject("Part::Feature",self.name+"_tableOutlineR")
        obj.Shape=self.tableOutlineR
        obj.Label=self.name+"_tableOutlineR"
        obj.ViewObject.ShapeColor=tuple([0.647,0.1647,0.1647])
        obj = doc.addObject("Part::Feature",self.name+"_eightballL")
        obj.Shape=self.eightballL
        obj.Label=self.name+"_eightballL"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_eightballR")
        obj.Shape=self.eightballR
        obj.Label=self.name+"_eightballR"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_eightball8L")
        obj.Shape=self.eightball8L
        obj.Label=self.name+"_eightball8L"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_eightball8R")
        obj.Shape=self.eightball8R
        obj.Label=self.name+"_eightball8R"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_bballL")
        obj.Shape=self.bballL
        obj.Label=self.name+"_bballL"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_bballR")
        obj.Shape=self.bballR
        obj.Label=self.name+"_bballR"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_bballBL")
        obj.Shape=self.bballBL
        obj.Label=self.name+"_bballBL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_bballBR")
        obj.Shape=self.bballBR
        obj.Label=self.name+"_bballBR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_aballL")
        obj.Shape=self.aballL
        obj.Label=self.name+"_aballL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_aballR")
        obj.Shape=self.aballR
        obj.Label=self.name+"_aballR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_aballAL")
        obj.Shape=self.aballAL
        obj.Label=self.name+"_aballAL"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_aballAR")
        obj.Shape=self.aballAR
        obj.Label=self.name+"_aballAR"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,0.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ballL")
        obj.Shape=self.l1ballL
        obj.Label=self.name+"_l1ballL"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ballR")
        obj.Shape=self.l1ballR
        obj.Label=self.name+"_l1ballR"
        obj.ViewObject.ShapeColor=tuple([1.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ballLL")
        obj.Shape=self.l1ballLL
        obj.Label=self.name+"_l1ballLL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l1ballLR")
        obj.Shape=self.l1ballLR
        obj.Label=self.name+"_l1ballLR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ballL")
        obj.Shape=self.l2ballL
        obj.Label=self.name+"_l2ballL"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ballR")
        obj.Shape=self.l2ballR
        obj.Label=self.name+"_l2ballR"
        obj.ViewObject.ShapeColor=tuple([0.0,0.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ballLL")
        obj.Shape=self.l2ballLL
        obj.Label=self.name+"_l2ballLL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_l2ballLR")
        obj.Shape=self.l2ballLR
        obj.Label=self.name+"_l2ballLR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubCL")
        obj.Shape=self.clubL[0]
        obj.Label=self.name+"_clubCL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubLL")
        obj.Shape=self.clubL[1]
        obj.Label=self.name+"_clubLL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubUL")
        obj.Shape=self.clubL[2]
        obj.Label=self.name+"_clubUL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubBL")
        obj.Shape=self.clubL[3]
        obj.Label=self.name+"_clubBL"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubCR")
        obj.Shape=self.clubR[0]
        obj.Label=self.name+"_clubCR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubLR")
        obj.Shape=self.clubR[1]
        obj.Label=self.name+"_clubLR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubUR")
        obj.Shape=self.clubR[2]
        obj.Label=self.name+"_clubUR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        obj = doc.addObject("Part::Feature",self.name+"_clubBR")
        obj.Shape=self.clubR[3]
        obj.Label=self.name+"_clubBR"
        obj.ViewObject.ShapeColor=tuple([1.0,1.0,1.0])
        self.boardL.show()
        self.boardR.show()

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    sign = SignBothSides("signBothSides",Base.Vector(0,0,0))
    sign.show()
    Gui.SendMsgToActiveView("ViewFit")
