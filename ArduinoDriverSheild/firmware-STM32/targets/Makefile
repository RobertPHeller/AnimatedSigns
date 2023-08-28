##-*- makefile -*-############################################################
#
#  System        : 
#  Module        : 
#  Object Name   : $RCSfile$
#  Revision      : $Revision$
#  Date          : $Date$
#  Author        : $Author$
#  Created By    : Robert Heller
#  Created       : Mon Apr 3 11:34:45 2023
#  Last Modified : <230828.1434>
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
##############################################################################


SUBDIRS = \
	freertos.armv7m.st-stm32f303re \
	freertos.armv7m.st-stm32f767zi
	
#\
#	freertos.armv7m.st-stm32l452re
	
include $(OPENMRNPATH)/etc/recurse.mk

flashf303:	all
	+$(MAKE) -C freertos.armv7m.st-stm32f303re flash
	
gdbf303:	flashf303
	+$(MAKE) -C freertos.armv7m.st-stm32f303re gdb
	

flashl452:      all
	+$(MAKE) -C freertos.armv7m.st-stm32l452re flash
	
gdbl452: flashl452
	+$(MAKE) -C freertos.armv7m.st-stm32l452re gdb

flashf767:      all
	+$(MAKE) -C freertos.armv7m.st-stm32f767zi flash
	
gdbf767: flashf767
	+$(MAKE) -C freertos.armv7m.st-stm32f767zi gdb
