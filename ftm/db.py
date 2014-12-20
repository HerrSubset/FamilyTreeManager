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
      events = []

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
        if birthDate != None:
          bdString = birthDate.text
          bdString = bdString.split("/")
          bd = dom.Date(bdString[0], bdString[1], bdString[2])
          tmp.setBirthDate(bd)

        passingDate = p.find("PassingDate")
        if passingDate != None:
          pString = passingDate.text
          pString = pString.split("/")
          pd = dom.Date(pString[0], pString[1], pString[2])
          tmp.setPassingDate(pd)

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

        #create household
        household = dom.Household(father, mother, children)

        #add wedding date if given
        weddingDate = h.find("WeddingDate")
        if weddingDate != None:
          wdString = weddingDate.text
          wdString = wdString.split("/")
          wd = dom.Date(wdString[0], wdString[1], wdString[2])
          household.setWeddingDate(wd)

        divorceDate = h.find("DivorceDate")
        if divorceDate != None:
          ddString = divorceDate.text
          ddString = ddString.split("/")
          dd = dom.Date(ddString[0], ddString[1], ddString[2])
          household.setDivorceDate(dd)

        #append household
        households.append(household)

      for e in root.iter("Event"):
        date = e.get("date")
        date = date.split("/")
        dateObject = dom.Date(date[0], date[1], date[2])

        description = e.get("description")

        event = dom.Event(description, dateObject)
        events.append(event)


      family = dom.Family()
      family.setFamilyMembers(familyMembers)
      family.setHouseholds(households)
      family.setEvents(events)

      return family



    def save(self, familyMembers, households, events, savePath):
      #TODO: split up the function
      root = ET.Element("Family")
      tree = ET.ElementTree()
      tree._setroot(root)

      m = ET.SubElement(root, "Members")
      e = ET.SubElement(root, "Events")
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

        passingDateObject = member.getPassingDate()
        if passingDateObject:
          passingDate = ET.SubElement(tmp, "PassingDate")
          passingDate.text = passingDateObject.toString()

      #add the households
      for household in households:
        #create element for current household
        tmp = ET.SubElement(h, "Household")

        #add id's of people in household
        father = ET.SubElement(tmp, "FatherID")
        father.text = "%d" % (household.getFather().getID())

        mother = ET.SubElement(tmp, "MotherID")
        mother.text = "%d" % (household.getMother().getID())

        #add wedding date if present
        dateObject = household.getWeddingDate()
        if dateObject:
          date = ET.SubElement(tmp, "WeddingDate")
          date.text = dateObject.toString()

        #add divorce date if present
        dateObject = household.getDivorceDate()
        if dateObject:
          divorceDate = ET.SubElement(tmp, "DivorceDate")
          divorceDate.text = dateObject.toString()

        children = ET.SubElement(tmp, "Children")

        #add all the children
        for child in household.getChildren():
          childTmp = ET.SubElement(children, "ChildID")
          childTmp.text = "%d" %(child.getID())

      for event in events:
        tmp = ET.SubElement(e, "Event")

        tmp.set("date", event.getDate().toString())
        tmp.set("description", event.getDescription())

      tree.write(savePath, "utf8", True)


    def getPerson(self, personID, people):
      res = None

      for p in people:
        if p.getID() == personID:
          res = p

      return res
