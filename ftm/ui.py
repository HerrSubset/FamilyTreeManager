import domain as dom

################################################################################
################################################################################
################################################################################
#CLInterface
################################################################################
################################################################################
################################################################################
class CLInterface(object):
  ##################################################
  #Constructor
  ##################################################
  def __init__(self, parametersContainer, family):
    self.pm = parametersContainer
    self.family = family

    self.defineAndStartAction()


  def defineAndStartAction(self):
    command = self.pm.getCommand()

    if command == "print":
      self.simplePrint()
    elif command == "update":
      self.update()
    elif command == "add":
      self.add()
    else:
      assert False, "Unknown command"

  ##################################################
  #Command functions
  ##################################################

  def simplePrint(self):
    res = ""

    #get filter variables
    pid = self.pm.getID()
    fid = self.pm.getFatherID()
    mid = self.pm.getMotherID()
    secondCommand = self.pm.getSecondCommand()

    #if person id is given, print person profile
    if pid:
      res = self.family.getProfile(pid)

    #if father and mother are given, print household profile
    elif fid != None and mid != None:
      res = self.family.getHouseholdProfile(fid, mid)

    #see if a special print command is given
    elif secondCommand:
      if secondCommand == "tree":
        print self.family.getTreeString()

      if secondCommand == "chronology":
        eventArray = self.family.getChronology()
        self.printChronology(eventArray)

      if secondCommand == "calendar":
        eventArray = self.family.getCalendar()
        self.printCalendar(eventArray)

    #if nothing is given, print family overview
    else:
      res = self.family.simplePrint()

    print res

  def update(self):
    #get parameter variables
    pid = self.pm.getID()
    fid = self.pm.getFatherID()
    mid = self.pm.getMotherID()
    startDateString = self.pm.getStartDateString()
    endDateString = self.pm.getEndDateString()
    phoneNumber = self.pm.getPhoneNumber()

    #update person
    if pid:
      if fid and mid:
        self.updateParents(pid, fid, mid)

      if startDateString:
        self.updateBirthday(pid, startDateString)

      if endDateString:
        self.updatePassingDate(pid, endDateString)

      if phoneNumber:
        self.updatePhoneNumber(pid, phoneNumber)

    #update household
    else:
      if self.pm.getFatherID() != None and self.pm.getMotherID() != None:
        self.family.createCouple(self.pm.getFatherID(), self.pm.getMotherID())
        print "Created Couple"

      if startDateString:
        tmp = startDateString.split("/")
        self.setWeddingDate(fid, mid, tmp[0], tmp[1], tmp[2])
        print "wedding date updated"

      if endDateString:
        self.updateDivorceDate(fid, mid, endDateString)

    #save changes
    self.family.save()

  def add(self):
    #get info
    name = self.pm.getName()
    familyName = self.pm.getFamilyName()
    gender = self.pm.getGender()
    startDateString = self.pm.getStartDateString()
    endDateString = self.pm.getEndDateString()
    fid = self.pm.getFatherID()
    mid = self.pm.getMotherID()


    if name and familyName and gender:
      #get id from created person to add additional info, if given
      pid = self.family.addFamilyMember(name, familyName, gender)
      print "Created new person"

      if fid and mid:
        self.updateParents(pid, fid, mid)

      if startDateString:
        self.updateBirthday(pid, startDateString)

      if endDateString:
        self.updatePassingDate(pid, endDateString)

    elif name and startDateString:
      tmp = startDateString.split("/")
      self.family.addEvent(name, tmp[0], tmp[1], tmp[2])
      print "Event added"

    else:
      print "Didn't know what to do"

    self.family.save()

  ##################################################
  #Update functions
  ##################################################
  def setBirthday(self, pid, day, month, year):
    self.family.addBirthday(pid, day, month, year)

  def setWeddingDate(self, fid, mid, day, month, year):
    self.family.addWeddingDate(fid, mid, day, month, year)

  def updateParents(self, pid, fid, mid):
    self.family.setParents(pid, fid, mid)
    print "Parents updated"

  def updateBirthday(self, pid, bdString):
    tmp = bdString.split("/")
    self.setBirthday(pid, tmp[0], tmp[1], tmp[2])
    print "Birthday updated"

  def updatePassingDate(self, pid, passingDate):
    tmp = passingDate.split("/")
    self.family.setPassingDay(pid, tmp[0], tmp[1], tmp[2])
    print "Passing date updated"

  def updateDivorceDate(self, fid, mid, divorceDate):
    tmp = divorceDate.split("/")
    self.family.setDivorceDate(fid, mid, tmp[0], tmp[1], tmp[2])
    print "Divorce date updated"

  def updatePhoneNumber(self, pid, phoneNumber):
    self.family.setPhoneNumber(pid, phoneNumber)
    print "Phone number updated"

  ##################################################
  #Update functions
  ##################################################
  def printChronology(self, eventArray):
    currentDate = None

    if eventArray[0]:
      currentDate = eventArray[0].getDate().getYear()

    for e in eventArray:
      s = "%s %s %s" % (e.getDate().toString(), e.getSign(), e.getDescription())

      if not(e.getDate().getYear() == currentDate):
        s = "\n" + s
        currentDate = e.getDate().getYear()

      print s

  def printCalendar(self, eventArray):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for i in range(12):
      print "\n%s:" % (months[i])
      for e in eventArray[i]:
        print "%s %s %s" % (e.getDate().toString(), e.getSign(), e.getDescription())
