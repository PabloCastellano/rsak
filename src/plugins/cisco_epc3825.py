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

from mechanize import Browser
import mechanize


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
		self.br = Browser()
		self.br.open("http://"+self.__class__.IP)
		self.br.select_form(nr=0)
		self.br["username_login"] = user
		self.br["password_login"] = passw
		self.br.submit()

		if self.br.geturl() != "http://192.168.1.1/Quick_setup.htm":
			print "Login failed"
			return False

		print "Login success"
		return True

	def getClientsList(self):
		req = self.br.open("http://192.168.1.1/DHCPReservation.htm")
		l = req.readlines()
		l2 = l[115:]
		i = 0
		while(l2[i] != '\n'):
			i = i+1
		l3 = l2[:i+1]

		for l in l3:
			print l

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
		print R.getClientsList()
		R.logout()
