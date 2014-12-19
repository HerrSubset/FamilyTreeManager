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
      self.addPerson()
    elif command == "printTree":
      self.printTree()
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

    #if person id is given, print person profile
    if pid:
      res = self.family.getProfile(pid)

    #if father and mother are given, print household profile
    elif fid != None and mid != None:
      res = self.family.getHouseholdProfile(fid, mid)

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

    #update person
    if pid:
      if fid and mid:
        self.family.setParents(pid, fid, mid)
        print "Parents updated"

      if startDateString:
        tmp = startDateString.split("/")
        self.setBirthday(pid, tmp[0], tmp[1], tmp[2])
        print "birthday updated"

    #update household
    else:
      if self.pm.getFatherID() != None and self.pm.getMotherID() != None:
        self.family.createCouple(self.pm.getFatherID(), self.pm.getMotherID())
        print "Created Couple"

      if startDateString:
        tmp = startDateString.split("/")
        self.setWeddingDate(fid, mid, tmp[0], tmp[1], tmp[2])
        print "wedding date updated"

    #save changes
    self.family.save()

  def addPerson(self):
    name = self.pm.getName()
    familyName = self.pm.getFamilyName()
    gender = self.pm.getGender()

    assert name != None, "Name is needed when adding person"
    assert familyName != None, "Family name is needed when adding person"
    assert gender != None, "Gender is needed when adding person"

    tmpID = self.family.addFamilyMember(name, familyName, gender)
    print "created new person"

    #TODO: check if other things can be added

    self.family.save()

  def printTree(self):
    print self.family.getTreeString()

  ##################################################
  #Update functions
  ##################################################
  def setBirthday(self, pid, day, month, year):
    self.family.addBirthday(pid, day, month, year)

  def setWeddingDate(self, fid, mid, day, month, year):
    self.family.addWeddingDate(fid, mid, day, month, year)
