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
        name = p.get("name")
        familyName = p.get("familyName")
        i = int(p.get("id"))
        gender = p.get("gender")

        #create person
        tmp = dom.Person(i, name, familyName, gender)

        #look for additional info
        birthDate = p.get("birthDate")
        if birthDate != None:
          bdString = birthDate.split("/")
          bd = dom.Date(bdString[0], bdString[1], bdString[2])
          tmp.setBirthDate(bd)

        passingDate = p.get("passingDate")
        if passingDate != None:
          pString = passingDate.split("/")
          pd = dom.Date(pString[0], pString[1], pString[2])
          tmp.setPassingDate(pd)

        phoneNumber = p.get("phoneNumber")
        if phoneNumber:
          tmp.setPhoneNumber(phoneNumber)

        #append person
        familyMembers.append(tmp)

      #create households
      for h in root.iter("Household"):
        #collect data
        father = self.getPerson(int(h.get("fatherID")), familyMembers)
        mother = self.getPerson(int(h.get("motherID")), familyMembers)
        children = []

        for child in h.iter("Child"):
          c = self.getPerson(int(child.get("id")), familyMembers)
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
        tmp.set("name", member.getName())
        tmp.set("familyName", member.getFamilyName())

        idString = "%d" % (member.getID())

        tmp.set("id", idString)
        tmp.set("gender", member.getGender())

        #store optional data
        dateObject = member.getBirthDate()
        if dateObject:
          tmp.set("birthDate", dateObject.toString())

        passingDateObject = member.getPassingDate()
        if passingDateObject:
          tmp.set("passingDate", passingDateObject.toString())

        phoneNumber = member.getPhoneNumber()
        if phoneNumber:
          tmp.set("phoneNumber", phoneNumber)

      #add the households
      for household in households:
        #create element for current household
        tmp = ET.SubElement(h, "Household")

        #add id's of people in household
        fidString = "%d" % (household.getFather().getID())
        tmp.set("fatherID", fidString)

        midString = "%d" % (household.getMother().getID())
        tmp.set("motherID", midString)

        #add wedding date if present
        dateObject = household.getWeddingDate()
        if dateObject:
          tmp.set("weddingDate", dateObject.toString())

        #add divorce date if present
        dateObject = household.getDivorceDate()
        if dateObject:
          tmp.set("divorceDate", dateObject.toString())

        children = ET.SubElement(tmp, "Children")

        #add all the children
        for child in household.getChildren():
          childTmp = ET.SubElement(children, "Child")
          childID = "%d" % (child.getID())
          childTmp.set("id", childID)

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
