#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rsak - Router Swiss Army Knife
# Copyright (C) 2011 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.# GPL

# Modelo

# Implementa interfaces
import os
import sys
sys.path.append(os.path.abspath(".."))
from routermodelbase import RouterModelBase
from ClientForm import ControlNotFoundError

from mechanize import Browser
import mechanize
import re


class RouterModel(RouterModelBase):

	MODEL = "CISCO EPC3825"
	URL = "http://www.cisco.com/web/consumer/support/modem_DPC3825.html"
	IP = "192.168.1.1"

	def __init__(self):
		print "loading", self.__class__.MODEL
		self.br = Browser()

	def guess(self):
		print "guessing"
		r = mechanize.urlopen("http://"+self.__class__.IP)
		l = r.readlines()

		return l[141] == "\t\t\t\t\tshowXHead('Cisco EPC3825 EuroDocsis 3.0 Gateway','EPC3825','@fw_version#',vstatus);\n"

	#Parece que autentica por IP, no por sesión
	#Si ya está logeado, peta por no encontrar el campo del formulario
	def login(self, user, passw):
		self.br.open("http://"+self.__class__.IP)
		self.br.select_form(nr=0)

		try:
			self.br["username_login"] = user
		except ControlNotFoundError:
			print "Already logged in"
			return True

		self.br["password_login"] = passw
		self.br.submit()

		if self.br.geturl() != "http://192.168.1.1/Quick_setup.htm":
			print "Login failed"
			return False

		print "Login success"
		return True

	#Devuelve lista con tuplas. [(ip, mac)]
	def getClientsList(self):
		req = self.br.open("http://192.168.1.1/DHCPReservation.htm")
		l = req.readlines()
		l2 = l[115:]
		i = 0
		while(l2[i] != '\n'):
			i = i+1
		l3 = l2[:i+1]

		MACexp=re.compile('^<TD width=200 ><FONT face=Arial color=#000000 size=2>(.*?)</FONT></TD>\n')
		IPexp=re.compile('<TD width=150 ><FONT face=Arial color=#000000 size=2>(.*?)</FONT></TD></TR>\n')
		maclist = []
		iplist = []

		for l in l3:
			if MACexp.search(l) != None:
				maclist.append(MACexp.search(l).group(1))
			elif IPexp.search(l) != None:
				iplist.append(IPexp.search(l).group(1))

		return zip(iplist, maclist)

	def logout(self):
		self.br.open("http://192.168.1.1/logout.htm")

#Port forwarding: http://192.168.1.1/AppGaming.htm
#Status: http://192.168.1.1/Status.htm

if __name__ == '__main__':
	print "main"
	R = RouterModel()
	print R.guess()
	#R.logout()
	if R.login("admin", "xxxxx"):
		clients = R.getClientsList()
		for c in clients:
			print "| %s\t| %s |" %(c[0], c[1])
		R.logout()
