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
#  Last Modified : <230905.1102>
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
    def printedPath(self,originOffset=Base.Vector(0,0,0),reverse=False):
        if reverse:
            rface = self.face.rotate(Base.Vector(21,0,0),Base.Vector(0,1,0),180)
            edges = rface.Edges
        else:
            edges = self.face.Edges
        p = None
        for e in edges:
            verts = e.Vertexes
            for v in verts:
                point = originOffset.add(Base.Vector(v.X,v.Y,0))
                if p==None:
                    p = path.path(path.moveto(point.x,point.y))
                else:
                    p.append(path.lineto(point.x,point.y))
        p.append(path.closepath())
        return p
        
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
        self.__ht = halfthichness
        #print("*** ArrowFace() halfthichness is ",halfthichness,file=sys.stderr)
        dx=tipx-tailx
        dy=tipy-taily
        #print("*** ArrowFace() dx,dy are ",dx,dy,file=sys.stderr)
        arrowlength= sqrt((dx*dx) + (dy*dy))
        self.__al = arrowlength
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
    def printedPath(self,originOffset=Base.Vector(0,0,0),reverse=False):
        if reverse:
            rface = self.face.rotate(Base.Vector(0+self.__al,0+self.__ht*2,0),Base.Vector(0,0,1),180)
            edges = rface.Edges
        else:
            edges = self.face.Edges
        p = None
        for e in edges:
            verts = e.Vertexes
            for v in verts:
                point = originOffset.add(Base.Vector(v.X,v.Y,0))
                if p==None:
                    p = path.path(path.moveto(point.x,point.y))
                else:
                    p.append(path.lineto(point.x,point.y))
        p.append(path.closepath())
        return p    
        

class WholeSignPath(object):
    __wholeSignPoly = [(5.715,5.08,0),(5.715,29.21,0),(10.16,29.21,0),(10.16,76.2,0),\
                      (31.75,76.2,0),(31.75,0,0),(10.16,0,0),(10.16,5.08,0),\
                      (5.715,5.08,0)]
    __printedSideRect = [(10.16,0),(31.75,0),(31.75,76.2),(10.16,76.2)]
    def __init__(self,origin):
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        polypoints = list()
        for tup in self.__wholeSignPoly:
            x,y,z = tup
            polypoints.append(origin.add(Base.Vector(x,y,z)))
        self.face=Part.Face(Part.Wire(Part.makePolygon(polypoints)))
    def printedPath(self,originOffset=Base.Vector(0,0,0)):
        p=None
        for tup in self.__printedSideRect:
            x,y = tup
            point = self.origin.add(originOffset.add(Base.Vector(x,y,0)))
            if p==None:
                p = path.path(path.moveto(point.x,point.y))
            else:
                p.append(path.lineto(point.x,point.y))
        p.append(path.closepath())
        return p

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

import os
import sys
sys.path.append(os.path.dirname(__file__))

from pyx import *

class SignBothSides(object):
    def __init__(self,name,origin):
        self.name=name
        if not isinstance(origin,Base.Vector):
            raise RuntimeError("origin is not a Vector!")
        self.origin=origin
        self.board = SignPCB(name+"_pcb",origin)
        self.__signcaseface = WholeSignPath(origin.add(Base.Vector(0,0,1.5)))
        self.caseL = self.__signcaseface.face.extrude(Base.Vector(0,0,1.1))
        self.caseL = self.caseL.cut(Part.makePlane(3.175,12.7,origin.add(Base.Vector(5.715,10.795,1.5))).extrude(Base.Vector(0,0,.5)))
        signcaseface = WholeSignPath(origin.add(Base.Vector(0,0,0)))
        self.caseR = signcaseface.face.extrude(Base.Vector(0,0,-1.1))
        self.caseR = self.caseR.cut(Part.makePlane(3.175,12.7,origin.add(Base.Vector(5.715,10.795,0))).extrude(Base.Vector(0,0,-.5)))
        self.__arrowface = ArrowFace(origin.add(Base.Vector(0,0,2.6)))        
        self.arrowL = self.__arrowface.face.extrude(Base.Vector(0,0,.1))
        arrowcut = ArrowFace(origin.add(Base.Vector(0,0,1.5))).face.extrude(Base.Vector(0,0,1.1))
        self.caseL = self.caseL.cut(arrowcut)
        arrowface = ArrowFace(origin.add(Base.Vector(0,0,-1.1)))
        self.arrowR = arrowface.face.extrude(Base.Vector(0,0,-.1))
        arrowcut = ArrowFace(origin.add(Base.Vector(0,0,0))).face.extrude(Base.Vector(0,0,-1.1))
        self.caseR = self.caseR.cut(arrowcut)
        cueface = VCueFace(origin.add(Base.Vector(0,0,2.6)))
        self.__cueface = cueface
        self.cueL = cueface.face.extrude(Base.Vector(0,0,.1))
        self.caseL = self.caseL.cut(cueface.CueCutout(1.5,1.1))
        cueface = VCueFace(origin.add(Base.Vector(0,0,-1.1)))
        self.cueR = cueface.face.extrude(Base.Vector(0,0,-.1))
        self.caseR = self.caseR.cut(cueface.CueCutout(0,-1.1))
        self.tableL = Part.makePlane(18-6.35,71.12-6.35,origin.add(Base.Vector(10.16+3.175,5.08+3.175,2.6))).extrude(Base.Vector(0,0,.1))
        self.tableR = Part.makePlane(18-6.35,71.12-6.35,origin.add(Base.Vector(10.16+3.175,5.08+3.175,-1.1))).extrude(Base.Vector(0,0,-.1))
        self.tableOutlineL = Part.makePlane(18,71.12,origin.add(Base.Vector(10.16,5.08,2.6))).extrude(Base.Vector(0,0,.1))
        self.tableOutlineR = Part.makePlane(18,71.12,origin.add(Base.Vector(10.16,5.08,-1.1))).extrude(Base.Vector(0,0,-.1))
        self.eightballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,2.6))))).extrude(Base.Vector(0,0,.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,1.5))))).extrude(Base.Vector(0,0,1.1)))
        self.eightballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,-1.1))))).extrude(Base.Vector(0,0,-.2))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,68,0))))).extrude(Base.Vector(0,0,-1.1)))
        tempL = Part.Face(Part.makeWireString("8","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy()
        self.__eightball8face = tempL.translate(origin.add(Base.Vector(19.16-2.5,68-3,2.6)))
        self.eightball8L = self.__eightball8face.extrude(Base.Vector(0,0,.3))
        self.eightball8R = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,68-3,-1.1))).extrude(Base.Vector(0,0,-.3))
        self.bballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,2.6))))).extrude(Base.Vector(0,0,.2))
        self.bballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,-1.1))))).extrude(Base.Vector(0,0,-.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,1.5))))).extrude(Base.Vector(0,0,1.1)))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,59,0))))).extrude(Base.Vector(0,0,-1.1)))
        tempL = Part.Face(Part.makeWireString("B","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.__bballBface = tempL.translate(origin.add(Base.Vector(19.16-2.5,59-3,2.6)))
        self.bballBL = self.__bballBface.extrude(Base.Vector(0,0,.3))
        self.bballBR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,59-3,-1.1))).extrude(Base.Vector(0,0,-.3))
        self.aballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,50,2.6))))).extrude(Base.Vector(0,0,.2))
        self.aballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,50,-1.1))))).extrude(Base.Vector(0,0,-.2))
        tempL = Part.Face(Part.makeWireString("A","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy()
        self.__aballAface = tempL.translate(origin.add(Base.Vector(19.16-2.5,50-3,2.6)))
        self.aballAL = self.__aballAface.extrude(Base.Vector(0,0,.3))
        self.aballAR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,50-3,-1.1))).extrude(Base.Vector(0,0,-.3))
        self.l1ballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,41,2.6))))).extrude(Base.Vector(0,0,.2))
        self.l1ballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,41,-1.1))))).extrude(Base.Vector(0,0,-.2))
        tempL = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.__l1ballL = tempL.translate(origin.add(Base.Vector(19.16-2.5,41-3,2.6))) 
        self.l1ballLL = self.__l1ballL.extrude(Base.Vector(0,0,.3))
        self.l1ballLR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,41-3,-1.1))).extrude(Base.Vector(0,0,-.3))
        self.l2ballL = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,2.6))))).extrude(Base.Vector(0,0,.2))
        self.l2ballR = Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,-1.1))))).extrude(Base.Vector(0,0,-.2))
        self.caseL = self.caseL.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,1.5))))).extrude(Base.Vector(0,0,1.1)))
        self.caseR = self.caseR.cut(Part.Face(Part.Wire(Part.makeCircle(4.572,origin.add(Base.Vector(19.16,32,0))))).extrude(Base.Vector(0,0,-1.1)))
        self.caseL = self.caseL.cut(Part.makePlane(4.572*2,59-32,origin.add(Base.Vector(19.16-4.572,32,1.5))).extrude(Base.Vector(0,0,1.1)))
        self.caseR = self.caseR.cut(Part.makePlane(4.572*2,59-32,origin.add(Base.Vector(19.16-4.572,32,0))).extrude(Base.Vector(0,0,-1.1)))
        tempL = Part.Face(Part.makeWireString("L","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",8,0.0)[0])
        tempR = tempL.copy() 
        self.__l2ballL = tempL.translate(origin.add(Base.Vector(19.16-2.5,32-3,2.6))) 
        self.l2ballLL = self.__l2ballL.extrude(Base.Vector(0,0,.3))
        self.l2ballLR = tempR.rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+2.5,32-3,-1.1))).extrude(Base.Vector(0,0,-.3))
        club = Part.makeWireString("CLUB","/usr/share/fonts/truetype/open-sans/","OpenSans-Bold.ttf",2.6,0.0)
        self.clubL = list()
        self.clubR = list()
        self.__clubFaces = list()
        self.__clubFaces.append(Part.Face(club[0]).translate(origin.add(Base.Vector(19.16-4,32-10,2.6))))
        self.__clubFaces.append(Part.Face(club[1]).translate(origin.add(Base.Vector(19.16-4,32-13,2.6))))
        self.__clubFaces.append(Part.Face(club[2]).translate(origin.add(Base.Vector(19.16-4,32-16,2.6))))
        self.__clubFaces.append(Part.Face(club[3]).translate(origin.add(Base.Vector(19.16-4,32-19,2.6))))
        self.clubL.append(self.__clubFaces[0].extrude(Base.Vector(0,0,.2)))
        self.clubL.append(self.__clubFaces[1].extrude(Base.Vector(0,0,.2)))
        self.clubL.append(self.__clubFaces[2].extrude(Base.Vector(0,0,.2)))
        self.clubL.append(self.__clubFaces[3].extrude(Base.Vector(0,0,.2)))
        self.clubR.append(Part.Face(club[0]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-10,-1.1))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[1]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-13,-1.1))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[2]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-16,-1.1))).extrude(Base.Vector(0,0,-.2)))
        self.clubR.append(Part.Face(club[3]).rotate(Base.Vector(0,0,0),Base.Vector(0,1,0),180).translate(origin.add(Base.Vector(19.16+4,32-19,-1.1))).extrude(Base.Vector(0,0,-.2)))
        self.caseL = self.caseL.cut(Part.makePlane(10,14,origin.add(Base.Vector(14,11,1.5))).extrude(Base.Vector(0,0,1.1)))
        self.caseR = self.caseR.cut(Part.makePlane(10,14,origin.add(Base.Vector(14,11,0))).extrude(Base.Vector(0,0,-1.1)))
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
        self.board.show()
    def __findTopFace(self,obj):
        for face in obj.Faces:
            bb = face.BoundBox
            if bb.ZLength == 0:
                #print("*** __findTopFace(): bb.XLength is %f and bb.YLength is %f"%(bb.XLength,bb.YLength),file=sys.stderr)
                if bb.XLength > 0 and bb.YLength > 0:
                    return face
    def __printedPathFrom3DRect(self,obj,originOffset=Base.Vector(0,0,0),reverse=False):
        topFace = self.__findTopFace(obj)
        if topFace == None:
            return path.path()
        if reverse:
            bb = topFace.rotate(Base.Vector(21,0,0),Base.Vector(0,1,0),180).BoundBox
        else:
            bb = topFace.BoundBox
        point = originOffset.add(Base.Vector(bb.XMin,bb.YMin,0))
        p = path.path(path.moveto(point.x,point.y))
        point = originOffset.add(Base.Vector(bb.XMin,bb.YMax,0))
        p.append(path.lineto(point.x,point.y))
        point = originOffset.add(Base.Vector(bb.XMax,bb.YMax,0))
        p.append(path.lineto(point.x,point.y))
        point = originOffset.add(Base.Vector(bb.XMax,bb.YMin,0))
        p.append(path.lineto(point.x,point.y))
        p.append(path.closepath())
        return p
    def __printedPathFrom3DCircle(self,obj,originOffset=Base.Vector(0,0,0),reverse=False):
        topFace = self.__findTopFace(obj)
        if topFace == None:
            return path.path()
        if reverse:
            bb = topFace.rotate(Base.Vector(21,0,0),Base.Vector(0,1,0),180).BoundBox
        else:
            bb = topFace.BoundBox
        center = originOffset.add(Base.Vector((bb.XMin+bb.XMax)/2.0,(bb.YMin+bb.YMax)/2.0,0))
        dia = (bb.XLength+bb.YLength)/2.0
        r = dia/2.0
        return path.path(path.arc(center.x,center.y,r,0,360))
    def __printedPathText(self,face,originOffset=Base.Vector(0,0,0),reverse=False):
        if reverse:
            rface = face.translate(Base.Vector(3.295,0,0))
            edges = rface.Edges
        else:
            edges = face.Edges
        p = None
        last = None
        for e in edges:
            verts = e.Vertexes
            newedge = True
            for v in verts:
                point = originOffset.add(Base.Vector(v.X,v.Y,0))
                if p==None:
                    p = path.path(path.moveto(point.x,point.y))
                else:
                    if newedge and point != last:
                        p.append(path.closepath())
                        p.append(path.moveto(point.x,point.y))
                    else:
                        p.append(path.lineto(point.x,point.y))
                last = point
                newedge = False
        p.append(path.closepath())
        return p
    def SignFace(self,filename='8BallSign.ps'):
        c = canvas.canvas()
        unit.set(defaultunit='mm')
        c.fill(self.__signcaseface.printedPath(Base.Vector(25.4,25.4,0)),[color.gray.black])
        c.fill(self.__arrowface.printedPath(Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,0)])
        c.fill(self.__cueface.printedPath(Base.Vector(25.4,25.4,0)),[color.gray.white])
        c.fill(self.__printedPathFrom3DRect(self.tableOutlineL,Base.Vector(25.4,25.4,0)),[color.rgb(0.647,0.1647,0.1647)])
        c.fill(self.__printedPathFrom3DRect(self.tableL,Base.Vector(25.4,25.4,0)),[color.rgb(0.0,1.0,0.0)])
        c.fill(self.__printedPathFrom3DCircle(self.eightballL,Base.Vector(25.4,25.4,0)),[color.rgb(0.0,0.0,0.0)])
        c.fill(self.__printedPathText(self.__eightball8face,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.bballL,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,0.0,0.0)])
        c.fill(self.__printedPathText(self.__bballBface,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.aballL,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,0.0)])
        c.fill(self.__printedPathText(self.__aballAface,Base.Vector(25.4,25.4,0)),[color.rgb(0.0,0.0,0.0)])
        c.fill(self.__printedPathFrom3DCircle(self.l1ballL,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,0.0,1.0)])
        c.fill(self.__printedPathText(self.__l1ballL,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.l2ballL,Base.Vector(25.4,25.4,0)),[color.rgb(0.0,0.0,1.0)])
        c.fill(self.__printedPathText(self.__l2ballL,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,1.0)])
        for cf in self.__clubFaces:
            c.fill(self.__printedPathText(cf,Base.Vector(25.4,25.4,0)),[color.rgb(1.0,1.0,1.0)])
        #
        c.fill(self.__signcaseface.printedPath(Base.Vector(76.2,25.4,0)),[color.gray.black])
        c.fill(self.__arrowface.printedPath(Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,0)])
        c.fill(self.__cueface.printedPath(Base.Vector(76.2,25.4,0),True),[color.gray.white])
        c.fill(self.__printedPathFrom3DRect(self.tableOutlineL,Base.Vector(76.2,25.4,0),True),[color.rgb(0.647,0.1647,0.1647)])        
        c.fill(self.__printedPathFrom3DRect(self.tableL,Base.Vector(76.2,25.4,0),True),[color.rgb(0.0,1.0,0.0)])
        c.fill(self.__printedPathFrom3DCircle(self.eightballL,Base.Vector(76.2,25.4,0),True),[color.rgb(0.0,0.0,0.0)])
        c.fill(self.__printedPathText(self.__eightball8face,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.bballL,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,0.0,0.0)])
        c.fill(self.__printedPathText(self.__bballBface,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.aballL,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,0.0)])
        c.fill(self.__printedPathText(self.__aballAface,Base.Vector(76.2,25.4,0),True),[color.rgb(0.0,0.0,0.0)])
        c.fill(self.__printedPathFrom3DCircle(self.l1ballL,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,0.0,1.0)])
        c.fill(self.__printedPathText(self.__l1ballL,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,1.0)])
        c.fill(self.__printedPathFrom3DCircle(self.l2ballL,Base.Vector(76.2,25.4,0),True),[color.rgb(0.0,0.0,1.0)])
        c.fill(self.__printedPathText(self.__l2ballL,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,1.0)])
        for cf in self.__clubFaces:
            c.fill(self.__printedPathText(cf,Base.Vector(76.2,25.4,0),True),[color.rgb(1.0,1.0,1.0)])
        #
        c.writePSfile(filename)        
        

if __name__ == '__main__':
    App.ActiveDocument=App.newDocument("Temp")
    doc = App.activeDocument()
    sign = SignBothSides("signBothSides",Base.Vector(0,0,0))
    sign.show()
    sign.SignFace()
    Gui.SendMsgToActiveView("ViewFit")
