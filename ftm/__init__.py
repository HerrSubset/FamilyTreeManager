import domain as dom

#ad = dom.Address("Liersesteenweg", 81, "Aarschot", 3200)
#bd = dom.Date(19,02,1992)
#bd2 = dom.Date(9,10,1994)
#p = dom.Person(1, "PJ", "smets", bd, ad, 'm')
#p2 = dom.Person(2, "Ruben", "smets", bd2, ad, 'm')
#p3 = dom.Person(3, "Johan", "smets", bd, ad, 'm')
#p4 = dom.Person(4, "Marianne", "verbraeken", bd2, ad, 'v')

#fam = dom.Family()

#fam.addFamilyMember(p)
#fam.addFamilyMember(p2)
#fam.addFamilyMember(p3)
#fam.addFamilyMember(p4)

#fam.addHousehold(p3, p4, [p, p2])


#print fam.toString()
#fam.printParents()
#print fam.getNextID()

fm = dom.FamilyManager()
'''
fm.addFamilyMember("Pieter-Jan", "Smets", 'M')
fm.addFamilyMember("Marianne", "Verbraeken", 'V')
fm.addFamilyMember("Johan", "Smets", 'M')
fm.addFamilyMember("Ruben", "Smets", 'M')

fm.addFamilyMember("Jelte", "Smets", 'M')
fm.addFamilyMember("Hilde", "Van Aerschot", 'V')
fm.addFamilyMember("Lotte", "Smets", 'V')
fm.addFamilyMember("Geert", "Smets", 'M')

fm.addFamilyMember("Jos", "Smets", 'M')
fm.addFamilyMember("Greta", "Houtmeyers", 'V')

fm.addFamilyMember("Bart", "Smets", 'M')
fm.addFamilyMember("Lut", "...", 'V')
fm.addFamilyMember("Lieze", "Smets", 'V')
fm.addFamilyMember("Sien", "Smets", 'V')

fm.setParents(1,3,2)
fm.setParents(4,3,2)

fm.setParents(5,8,6)
fm.setParents(7,8,6)

fm.setParents(3,9,10)
fm.setParents(8,9,10)
fm.setParents(11,9,10)

fm.setParents(13,11,12)
fm.setParents(14,11,12)
'''
fm.load()
print fm.getMemberOverview()
print fm.extensivePrint()
#fm.save()
