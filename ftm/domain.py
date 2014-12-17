import db

###############################################################################
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
    def __init__(self, family = None):
        if family == None:
            self.family = Family()
            self.writer = db.XMLWriter()
        else:
            self.family = family

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
    def addFamilyMember(self, name, familyName, gender):
        tmpID = self.family.getNextID()
        tmp = Person(tmpID, name, familyName, gender)

        self.family.addFamilyMember(tmp)

    def setAddress(self, pid, day, month, year):
        tmp = Address(day, month, year)
        p = self.family.getMember(pid)

        if p != None:
            p.setAddress(tmp)

    def setParents(self, childID, fatherID, motherID):
        self.family.setParents(childID, fatherID, motherID)


    def getMemberOverview(self):
        return self.family.getMemberOverview()

    def extensivePrint(self):
        return self.family.toString()

    def save(self):
      self.writer.save(self.family.getMembers(), self.family.getHouseholds())
      
    def load(self):
      self.family = self.writer.load()



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

    ##################################################
    #setters
    ##################################################
    def setFamilyMembers(self, familyMembers):
      self.familyMembers = familyMembers
    def setHouseholds(self, households):
      self.households = households

    ##################################################
    #getters
    ##################################################
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

    def getMembers(self):
      return self.familyMembers

    def getHouseholds(self):
      return self.households

    ##################################################
    #other functions
    ##################################################
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

        tmp = Household(f, m, c)
        self.households.append(tmp)

    def addChildToHousehold(self, childID, fatherID, motherID):
        for h in self.households:
            fid = h.getFather().getID()
            mid = h.getMother().getID()

            if fid == fatherID and mid == motherID:
                h.addChild(self.getMember(childID))


    ##################################################
    #family checkers
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
    def getMemberOverview(self):
        res = "\n"

        for m in self.familyMembers:
            tmp = "%d: %s %s\n" % (m.getID(), m.getName(), m.getFamilyName())
            res = res + tmp

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

    ##################################################
    #getters
    ##################################################
    def getFather(self):
        return self.father
    def getMother(self):
        return self.mother
    def getChildren(self):
        return self.children

    ##################################################
    #setters
    ##################################################


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

    def isMotherOf(self, childID, motherID):
        res = False

        if self.isChild(childID) and self.mother.getID() == motherID:
            res = True

        return res

    def toString(self):
        fa = "\nFather:\t%s %s\n"%(self.father.getName(), self.father.getFamilyName())
        mo = "Mother:\t%s %s\n"%(self.mother.getName(), self.mother.getFamilyName())
        ch = "Children:\n"
        for child in self.children:
            tmp = "\t%s %s\n" % (child.getName(), child.getFamilyName())
            ch = ch + tmp

        return fa + mo + ch





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
    def setFamilyName(self, familyName):
        self.familyName = familyName
    def setName(self, name):
        self.name = name

    ##################################################
    #other functions
    ##################################################
    def toString(self):
        nString = "\nName:\t\t%s\n" %(self.name)
        idString = "ID:\t\t%d\n" % (self.getID())
        fnString = "Family Name:\t%s\n" % (self.familyName)
        if not (self.birthDate == None):
            bdString = "Birthday:\t%s\n" % (self.getBirthDate().toString())
        else:
            bdString = ""
        if not (self.address == None):
            adString = "Address:\t%s\n" % (self.getAddress().toString())
        else:
            adString = ""
        gnString = "Gender:\t\t%s\n" % (self.getGender())
        return nString + idString + fnString + bdString + adString + gnString





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

    ##################################################
    #other functions
    ##################################################
    def toString(self):
        res = "%d/%d/%d" %(self.day, self.month, self.year)
        return res
