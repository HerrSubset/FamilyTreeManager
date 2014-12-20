import db, getopt
import os.path

################################################################################
################################################################################
################################################################################
#FamilyManager class
################################################################################
################################################################################
################################################################################
class FamilyManager(object):
    ##################################################
    #constructor
    ##################################################
    def __init__(self, parametersContainer = None, family = None,):
        if family == None:
            self.family = Family()
            self.writer = db.XMLWriter()
        else:
            self.family = family
        if parametersContainer != None:
          self.pc = parametersContainer

        if self.pc != None and os.path.isfile(self.pc.getSavePath()) :
          self.load(self.pc.getSavePath())

    ##################################################
    #getters
    ##################################################
    def getFamily(self):
        return self.family

    ##################################################
    #setters
    ##################################################
    def setFamily(self, family):
        self.family = family

    ##################################################
    #other functions
    ##################################################
    def addEvent(self, name, day, month, year):
      d = Date(day, month, year)
      e = Event(name, d)

      self.family.addEvent(e)

    def addFamilyMember(self, name, familyName, gender):
        tmpID = self.family.getNextID()
        tmp = Person(tmpID, name, familyName, gender)

        self.family.addFamilyMember(tmp)
        #return ID in case you want to add stuff to the new person
        return tmpID

    def addBirthday(self, pid, day, month, year):
      p = self.family.getMember(pid)
      tmp = Date(day, month, year)

      if p:
        p.setBirthDate(tmp)

    def setPassingDay(self, pid, day, month, year):
      p = self.family.getMember(pid)
      tmp = Date(day, month, year)

      if p:
        p.setPassingDate(tmp)

    def setDivorceDate(self, fid, mid, day, month, year):
      h = self.family.getHousehold(fid, mid)
      tmp = Date(day, month, year)

      if h:
        h.setDivorceDate(tmp)

    def addWeddingDate(self, fid, mid, day, month, year):
      h = self.family.getHousehold(fid, mid)
      tmp = Date(day, month, year)

      if h:
        h.setWeddingDate(tmp)

    def setParents(self, childID, fatherID, motherID):
      self.family.setParents(childID, fatherID, motherID)

    def createCouple(self, fatherID, motherID):
      self.family.addHousehold(fatherID, motherID)

    def getTreeString(self):
      return self.family.getTreeString()

    def getMemberOverview(self):
      return self.family.getMemberOverview()

    def getProfile(self, pid):
      return self.family.getProfile(pid)

    def getHouseholdProfile(self, fid, mid):
      return self.family.getHouseholdProfile(fid, mid)

    def getChronology(self):
      return self.family.getChronology()

    def getCalendar(self):
      return self.family.getCalendar()

    def simplePrint(self):
      return self.family.toStringSimple()

    def extensivePrint(self):
      return self.family.toString()

    def save(self):
      memb = self.family.getMembers()
      hous = self.family.getHouseholds()
      even = self.family.getEvents()
      path = self.pc.getSavePath()
      self.writer.save(memb, hous, even, path)

    def load(self, savePath):
      self.family = self.writer.load(savePath)



################################################################################
################################################################################
################################################################################
#Family class
################################################################################
################################################################################
################################################################################
class Family(object):
    ##################################################
    #constructor
    ##################################################
    def __init__(self):
        self.familyMembers = []
        self.households = []
        self.events = []

    ##################################################
    #setters
    ##################################################
    def setFamilyMembers(self, familyMembers):
      self.familyMembers = familyMembers
    def setHouseholds(self, households):
      self.households = households
    def setEvents(self, events):
      self.events = events

    ##################################################
    #getters
    ##################################################
    def getMembers(self):
      return self.familyMembers
    def getHouseholds(self):
      return self.households
    def getEvents(self):
      return self.events

    def getMember(self, pid):
        res = None

        for m in self.familyMembers:
            if m.getID() == pid:
                res = m

        return res

    def getNextID(self):
        res = 1

        for m in self.familyMembers:
            if m.getID() >= res:
                res = m.getID() + 1

        return res

    def getFamilyFatherID(self):
      res = 0

      #pick household and check if father or mother has a parent, pick that
      #parents' household until neither parent has a parent
      if len(self.households) > 0:
        rootH = self.getRootHousehold(self.households[0])
        res = rootH.getFather().getID()


      return res

    def getChildsHousehold(self, childID):
      res = None

      for h in self.households:
        if h.isChild(childID):
          res = h

      return res

    def getRootHousehold(self, household):
      res = household

      #create variables for easier reading
      fatherIsChild = self.isChild(household.getFather().getID())
      motherIsChild = self.isChild(household.getMother().getID())

      #check which parent has parents. Continue searching on the branch where
      #parents exist. If neither have parents you found the root houshold
      if fatherIsChild:
        tmp = self.getChildsHousehold(household.getFather().getID())
        res = self.getRootHousehold(tmp)

      elif motherIsChild:
        tmp = self.getChildsHousehold(household.getMother().getID())
        res = self.getRootHousehold(tmp)


      return res

    def getRelationships(self, parentID):
      #TODO: return all the households in which parentID is a parent
      res = None

      for h in self.households:
        if parentID in (h.getFather().getID(), h.getMother().getID()):
          res = h

      return res

    def getHousehold(self, fid, mid):
      res = None

      for h in self.households:
        if mid == h.getMother().getID() and fid == h.getFather().getID():
          res = h

      return res

    def getChronology(self):
      res = []

      #add birthdays and deaths
      for m in self.familyMembers:
        birthDate = m.getBirthDate()
        passingDate = m.getPassingDate()

        if birthDate:
          bdString = "%s %s" % (m.getName(), m.getFamilyName())
          bdEvent = Event(bdString, birthDate, "o")
          res.append(bdEvent)

        if passingDate:
          pdString = "%s %s" % (m.getName(), m.getFamilyName())
          pdEvent = Event(pdString, passingDate, "+")
          res.append(pdEvent)


      for h in self.households:
        weddingDate = h.getWeddingDate()
        coupleString = h.getParentsString()

        if weddingDate:
          e = Event(coupleString, weddingDate)
          res.append(e)

      for event in self.events:
        res.append(event)

      res = self.sortEvents(res)
      return res

    def getCalendar(self):
      res = []

      #create empty array for every month
      for i in range(0,12):
        res.append([])

      #get event list
      events = self.getChronology()

      #put events in correct month
      for e in events:
        res[e.getDate().getMonth() - 1].append(e)

      #sort every month
      for i in range(12):
        res[i] = self.sortEventsWithoutYear(res[i])

      return res

    ##################################################
    #other functions
    ##################################################
    def addEvent(self, e):
      self.events.append(e)

    def addFamilyMember(self, p):
        #TODO: build in checks to see if person isn't added already and that the
        #thing added is actually a person
        self.familyMembers.append(p)

    def setParents(self, childID, fatherID, motherID):
        if ( not self.isChild(childID)) and (self.haveFamily(fatherID, motherID)):
            self.addChildToHousehold(childID, fatherID, motherID)

        elif (not self.isChild(childID)) and (not self.haveFamily(fatherID, motherID)):
            self.addHousehold(fatherID, motherID, [childID])

    def addHousehold(self, fatherID, motherID, children = []):
        f = self.getMember(fatherID)
        m = self.getMember(motherID)
        c = []
        for ch in children:
            c.append(self.getMember(ch))

        h = self.getHousehold(fatherID, motherID)
        if h == None:
          tmp = Household(f, m, c)
          self.households.append(tmp)
        else:
          pass
          #TODO: throw error (couple already exists)

    def addChildToHousehold(self, childID, fatherID, motherID):
        for h in self.households:
            fid = h.getFather().getID()
            mid = h.getMother().getID()

            if fid == fatherID and mid == motherID:
                h.addChild(self.getMember(childID))

    def sortEvents(self, events):
      isSorted = False

      while not isSorted:
        isSorted = True
        for i in range(len(events) - 1):
          firstDate = events[i].getDate()
          secondDate = events[i+1].getDate()

          if secondDate.isEarlierThan(firstDate):
            isSorted = False
            events[i], events[i+1] = events[i+1], events[i]

      return events

    def sortEventsWithoutYear(self, events):
      isSorted = False

      while not isSorted:
        isSorted = True
        for i in range(len(events) - 1):
          firstDate = events[i].getDate()
          secondDate = events[i+1].getDate()

          if secondDate.fallsEarlierThan(firstDate):
            isSorted = False
            events[i], events[i+1] = events[i+1], events[i]

      return events

    ##################################################
    #family boolean checkers
    ##################################################
    def isFatherOf(self, childID, fatherID):
        res = false

        for h in households:
            if h.isFatherOf(childID,fatherID):
                res = True

        return res

    def isMother(self, motherID):
        res = False

        for h in self.households:
            if h.getMother().getID() == motherID:
                res = True

        return res

    def isMotherOf(self, childID, motherID):
        res = false

        for h in households:
            if h.isMotherOf(childID,motherID):
                res = true

        return res

    def isFather(self, fatherID):
        res = False

        for h in self.households:
            if h.getFather().getID() == fatherID:
                res = True

        return res

    def isChild(self, childID):
        res = False

        for h in self.households:
            if h.isChild(childID):
                res = True

        return res

    def haveFamily(self, fatherID, motherID):
        res = False

        for h in self.households:
            fid = h.getFather().getID()
            mid = h.getMother().getID()
            if fid == fatherID and mid == motherID:
                res = True

        return res

    ##################################################
    #string functions
    ##################################################
    def getProfile(self, pid):
      member = self.getMember(pid)
      return member.toString()

    def getHouseholdProfile(self, fid, mid):
      household = self.getHousehold(fid, mid)
      return household.toString()

    def getIndentationString(self, level):
      res = ""

      for i in range(level):
        res = res + "|\t"

      return res + "+--"


    def getTreeString(self, ID = 0, level = 0):
      res = ""

      #if an ID is given, create tree from there. Otherwise look for family root
      if ID == 0:
        ID = self.getFamilyFatherID()

      #get household you're currently printing
      rootHousehold = self.getRelationships(ID)

      #if current id has no family, simply print the name
      if rootHousehold == None:
        name = self.getMember(ID).getName()
        fName = self.getMember(ID).getFamilyName()
        iString = self.getIndentationString(level)
        res = res + iString + name + " " + fName + "\n"

      #otherwise print the entire household
      else:
        fatherN = rootHousehold.getFather().getName()
        fatherFM = rootHousehold.getFather().getFamilyName()

        motherN = rootHousehold.getMother().getName()
        motherFN = rootHousehold.getMother().getFamilyName()

        res = res + self.getIndentationString(level)

        res = res + "%s %s X %s %s\n" % (fatherN, fatherFM, motherN, motherFN)

        for child in rootHousehold.getChildren():
          res = res + self.getTreeString(child.getID(), level + 1)

      return res

    def getMemberOverview(self):
        res = "\n"

        for m in self.familyMembers:
            tmp = "%s %s (%d)\n" % (m.getName(), m.getFamilyName(), m.getID())
            res = res + tmp

        return res

    def toStringSimple(self):
      res = ""

      for member in self.familyMembers:
        res = res + member.toStringSimple()

      for household in self.households:
        res = res + household.toString()

      return res

    def toString(self):
        res = ""

        for member in self.familyMembers:
            res = res + member.toString()

        for household in self.households:
            res = res + household.toString()

        return res

    ##################################################
    #Developer functions
    ##################################################
    def printParents(self):
        res =  "\nFathers:\n"
        for m in self.familyMembers:
            if self.isFather(m.getID()):
                res = res + "\t" + m.getName() + " " + m.getFamilyName() + "\n"

        print "Mothers:"
        for m in self.familyMembers:
            if self.isMother(m.getID()):
                res = res + "\t" + m.getName() + " " + m.getFamilyName() + "\n"

        return res



################################################################################
################################################################################
################################################################################
#Household class
################################################################################
################################################################################
################################################################################
class Household(object):
  ##################################################
  #constructor
  ##################################################
  def __init__(self, father = None, mother = None, children = []):
    self.father = father
    self.mother = mother
    self.children = children
    self.weddingDate = None
    self.divorceDate =None

  ##################################################
  #getters
  ##################################################
  def getFather(self):
    return self.father
  def getMother(self):
    return self.mother
  def getChildren(self):
    return self.children
  def getWeddingDate(self):
    return self.weddingDate
  def getDivorceDate(self):
    return self.divorceDate

  ##################################################
  #setters
  ##################################################
  def setWeddingDate(self, weddingDate):
    self.weddingDate = weddingDate
  def setDivorceDate(self, divorceDate):
    self.divorceDate = divorceDate

  ##################################################
  #other functions
  ##################################################
  def addChild(self, child):
    self.children.append(child)

  def isChild(self, childID):
    res = False

    for child in self.children:
      if child.getID() == childID:
        res = True

    return res

  def isFatherOf(self, childID, fatherID):
    res = False

    if self.isChild(childID) and self.father.getID() == fatherID:
      res = True

    return res

  def getParentsString(self):
    #TODO: print bloodline member first
    res = ""

    motherName = "%s %s" % (self.mother.getName(), self.mother.getFamilyName())
    fatherName = "%s %s" % (self.father.getName(), self.father.getFamilyName())
    res = "%s X %s" % (fatherName, motherName)

    return res

  def isMotherOf(self, childID, motherID):
    res = False

    if self.isChild(childID) and self.mother.getID() == motherID:
      res = True

    return res

  def toString(self):
    fa = "\nFather:\t\t%s"%(self.father.toStringSimple())
    mo = "Mother:\t\t%s"%(self.mother.toStringSimple())

    we = ""
    if self.weddingDate:
      we = "Wedding Date:\t%s\n" % (self.weddingDate.toString())

    di = ""
    if self.divorceDate:
      di = "Divorce Date:\t%s\n" % (self.divorceDate.toString())

    ch = "Children:\n"
    for child in self.children:
      tmp = "\t\t%s" % (child.toStringSimple())
      ch = ch + tmp

    return fa + mo + we + di + ch





################################################################################
################################################################################
################################################################################
#Person class
################################################################################
################################################################################
################################################################################
class Person(object):
    ##################################################
    #constructors
    ##################################################
    def __init__(self, ID, name, familyName, gender='?', birthDate=None, address=None):
        self.name = name
        self.familyName = familyName
        self.birthDate = birthDate
        self.passingDate = None
        self.address = address
        self.gender = gender
        self.ID = int(ID)

    ##################################################
    #getters
    ##################################################
    def getName(self):
      return self.name
    def getFamilyName(self):
      return self.familyName
    def getBirthDate(self):
      return self.birthDate
    def getPassingDate(self):
      return self.passingDate
    def getAddress(self):
      return self.address
    def getGender(self):
      return self.gender
    def getID(self):
      return self.ID

    ##################################################
    #setters
    ##################################################
    def setGender(self, gender):
      self.gender = gender
    def setAddress(self, address):
      self.address = address
    def setBirthDate(self, birthDate):
      self.birthDate = birthDate
    def setPassingDate(self, passingDate):
      self.passingDate = passingDate
    def setFamilyName(self, familyName):
      self.familyName = familyName
    def setName(self, name):
      self.name = name

    ##################################################
    #other functions
    ##################################################
    def toStringSimple(self):
      return "%s %s (id: %d)\n" % (self.name, self.familyName, self.ID)

    def toString(self):
      #basic variables
      nString = "Name:\t\t%s\n" %(self.name)
      idString = "ID:\t\t%d\n" % (self.getID())
      fnString = "Family Name:\t%s\n" % (self.familyName)
      bdString = ""
      pString = ""
      adString = ""

      #fill in optional variables
      if self.birthDate != None:
        bdString = "Birthday:\t%s\n" % (self.getBirthDate().toString())

      if self.passingDate != None:
        pString = "Passed on:\t%s\n" % (self.getPassingDate().toString())

      if self.address != None:
        adString = "Address:\t%s\n" % (self.getAddress().toString())

      gnString = "Gender:\t\t%s\n" % (self.getGender())
      return idString + nString + fnString + bdString + pString + adString + gnString





################################################################################
################################################################################
################################################################################
#Address class
################################################################################
################################################################################
################################################################################
class Address(object):
    ##################################################
    #constructors
    ##################################################
    def __init__(self, street, streetNumber, town, zipCode):
        self.street = street
        self.streetNumber = streetNumber
        self.town = town
        self.zipCode = zipCode

    ##################################################
    #getters
    ##################################################
    def getStreet(self):
        return self.street
    def getStreetNumber(self):
        return self.streetNumber
    def getTown(self):
        return self.town
    def getZipCode(self):
        return self.zipCode

    ##################################################
    #setters
    ##################################################
    def setZipCode(self, zipCode):
        self.zipCode = zipCode
    def setTown(self, town):
        self.town = town
    def setStreetNumber(self, streetNumber):
        self.streetNumber = streetNumber
    def setStreet(self, street):
        self.street = street

    ##################################################
    #other functions
    ##################################################
    def toString(self):
        res = "%s %d, %d %s" %(self.street, self.streetNumber, self.zipCode, self.town)
        return res





################################################################################
################################################################################
################################################################################
#Date class
################################################################################
################################################################################
################################################################################

class Date(object):
    ##################################################
    #Constructor
    ##################################################
    def __init__(self, day, month, year):
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)

    ##################################################
    #Getters
    ##################################################
    def getDay(self):
      return self.day

    def getMonth(self):
      return self.month

    def getYear(self):
      return self.year

    def getDecennium(self):
      res = self.year - ((self.year/1000)*1000)
      res = res - ((self.year/100)*100)
      res = res / 10 * 10

    ##################################################
    #other functions
    ##################################################
    def asInteger(self):
      return (self.year * 10000) + (self.month * 100) + self.day

    def asIntegerWithoutYear(self):
      return (self.month * 100) + self.day

    def compare(self, d):
      return d.asInteger() - self.asInteger()

    def isEarlierThan(self, d):
      res = False

      if self.asInteger() < d.asInteger():
        res = True

      return res

    def fallsEarlierThan(self, d):
      res = False

      if self.asIntegerWithoutYear() < d.asIntegerWithoutYear():
        res = True

      return res

    def toString(self):
      day = ""
      if self.day < 10:
        day = "0%d" % (self.day)
      else:
        day = "%d" % (self.day)

      month = ""
      if self.month < 10:
        month = "0%d" % (self.month)
      else:
        month = "%d" % (self.month)

      year = "%d" % (self.year)

      return "%s/%s/%s" % (day, month, year)





################################################################################
################################################################################
################################################################################
#ParametersContainer
################################################################################
################################################################################
################################################################################
class Event(object):
  ##################################################
  #Constructor
  ##################################################
  def __init__(self, description, date, sign = " "):
    self.description = description
    self.date = date
    self.sign = sign

  ##################################################
  #Getters
  ##################################################
  def getDescription(self):
    return self.description
  def getDate(self):
    return self.date
  def getSign(self):
    return self.sign





################################################################################
################################################################################
################################################################################
#ParametersContainer
################################################################################
################################################################################
################################################################################
class ParametersContainer(object):
  def __init__(self, arg):
    self.arguments = self.buildArguments(arg)

  def buildArguments(self, arg):
    res = {}

    #set defaults
    res["savePath"] = "./family.xml"
    try:
      res["command"] = arg[1]
      #TODO: check if command is valid
    except IndexError as err:
      print "No command given"
      print "exiting"
      exit(2)

    #process arg variable
    try:
      opts, args = getopt.getopt(arg[2:], "n:N:i:f:m:g:F:d:D:")
    except getopt.GetoptError as err:
      # print help information and exit:
      print str(err)
      sys.exit(2)

    #extract parameters
    for o,a in opts:
      if o == "-n":
        res["name"] = a
      elif o == "-N":
        res["familyname"] = a
      elif o == "-i":
        res["id"] = int(a)
      elif o == "-f":
        res["fatherID"] = int(a)
      elif o == "-m":
        res["motherID"] = int(a)
      elif o == "-g":
        res["gender"] = a
      elif o == "-F":
        res["savePath"] = a
      elif o == "-d":
        res["startDateString"] = a
      elif o == "-D":
        res["endDateString"] = a
      else:
        print "gave option" + o
        assert False, "Unhandeled option"

    try:
      res["secondCommand"] = args[0]
    except IndexError as err:
      pass

    return res

  ##################################################
  #getters
  ##################################################
  def getName(self):
    res = None

    try:
      res = self.arguments["name"]
    except KeyError as err:
      res = None

    return res

  def getFamilyName(self):
    res = None
    try:
      res = self.arguments["familyname"]
    except KeyError as err:
      res = None

    return res

  def getID(self):
    res = None
    try:
      res = self.arguments["id"]
    except KeyError as err:
      res = None

    return res

  def getGender(self):
    res = None
    try:
      res = self.arguments["gender"]
    except KeyError as err:
      res = None

    return res

  def getMotherID(self):
    res = None
    try:
      res = self.arguments["motherID"]
    except KeyError as err:
      res = None

    return res

  def getFatherID(self):
    res = None
    try:
      res = self.arguments["fatherID"]
    except KeyError as err:
      res = None

    return res

  def getStartDateString(self):
    res = None
    try:
      res = self.arguments["startDateString"]
    except KeyError as err:
      res = None

    return res

  def getEndDateString(self):
    res = None
    try:
      res = self.arguments["endDateString"]
    except KeyError as err:
      res = None

    return res

  def getSecondCommand(self):
    res = None
    try:
      res = self.arguments["secondCommand"]
    except KeyError as err:
      res = None

    return res

  def getCommand(self):
    return self.arguments["command"]
  def getSavePath(self):
    return self.arguments["savePath"]
