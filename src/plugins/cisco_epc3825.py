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


class RouterModel(RouterModelBase):

	MODEL = "CISCO EPC3825"
	URL = "http://www.cisco.com/web/consumer/support/modem_DPC3825.html"

	def __init__(self):
		print "loading"

if __name__ == '__main__':
	print "main"
