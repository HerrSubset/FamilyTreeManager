import domain as dom
import ui
from sys import argv

pc = dom.ParametersContainer(argv)
fm = dom.FamilyManager(pc)
interface = ui.CLInterface(pc, fm)
