import xml.etree.ElementTree as ET
import domain as dom
###############################################################################
################################################################################
################################################################################
#XMLWriter class
################################################################################
################################################################################
################################################################################
class XMLWriter(object):
    def __init__(self):
      pass

    def load(self, savePath):
      tree = ET.parse(savePath)
      root = tree.getroot()

      familyMembers = []
      households = []

      #create family members
      for p in root.iter("Person"):
        #collect data
        name = p.find("Name").text
        familyName = p.find("Familyname").text
        i = int(p.find("ID").text)
        gender = p.find("Gender").text

        #create person
        tmp = dom.Person(i, name, familyName, gender)

        #look for additional info
        birthDate = p.find("BirthDate")
        bd = None
        if birthDate != None:
          bdString = birthDate.text
          bdString = bdString.split("/")
          bd = dom.Date(bdString[0], bdString[1], bdString[2])
          tmp.setBirthDate(bd)

        #append person
        familyMembers.append(tmp)

      #create households
      for h in root.iter("Household"):
        #collect data
        father = self.getPerson(int(h.find("FatherID").text), familyMembers)
        mother = self.getPerson(int(h.find("MotherID").text), familyMembers)
        children = []

        for child in h.iter("ChildID"):
          c = self.getPerson(int(child.text), familyMembers)
          children.append(c)

        #create and append household
        household = dom.Household(father, mother, children)
        households.append(household)

      family = dom.Family()
      family.setFamilyMembers(familyMembers)
      family.setHouseholds(households)

      return family



    def save(self, familyMembers, households, savePath):
      #TODO: split up the function
      root = ET.Element("Family")
      tree = ET.ElementTree()
      tree._setroot(root)

      m = ET.SubElement(root, "Members")
      h = ET.SubElement(root, "Households")

      #add the family members
      for member in familyMembers:
        #create element for current member
        tmp = ET.SubElement(m, "Person")

        #add data to current member's element
        name = ET.SubElement(tmp, "Name")
        name.text = member.getName()

        fname = ET.SubElement(tmp, "Familyname")
        fname.text = member.getFamilyName()

        i = ET.SubElement(tmp, "ID")
        i.text = "%d" % (member.getID())

        gend = ET.SubElement(tmp, "Gender")
        gend.text = member.getGender()

        dateObject = member.getBirthDate()
        if dateObject:
          date = ET.SubElement(tmp, "BirthDate")
          date.text = dateObject.toString()

      #add the households
      for household in households:
        #create element for current household
        tmp = ET.SubElement(h, "Household")

        #add id's of people in household
        father = ET.SubElement(tmp, "FatherID")
        father.text = "%d" % (household.getFather().getID())

        mother = ET.SubElement(tmp, "MotherID")
        mother.text = "%d" % (household.getMother().getID())

        children = ET.SubElement(tmp, "Children")

        #add all the children
        for child in household.getChildren():
          childTmp = ET.SubElement(children, "ChildID")
          childTmp.text = "%d" %(child.getID())

      tree.write(savePath, "utf8", True)


    def getPerson(self, personID, people):
      res = None

      for p in people:
        if p.getID() == personID:
          res = p

      return res
