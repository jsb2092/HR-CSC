from spot_processing import Station



def main():

    bands = {}
    states = []
    countries = []
    dxcc = []
    multiplier = 0
    bandStates = {}
    bandDXCC = {}

    filename = input("Enter Cabrio filename: ")
    multiband = False
    multiplerCountry = False
    m = input("Is the multiplier a multiband multiplier (for the same contact) [Y/N]: ")
    m2 = input("Is the DX multipler by contact (Select Y only if you get 1 multiplier for each DXCC)? [Y/N]: ")

    if m.upper() == "Y":
        multiband = True
    if m2.upper() == "Y":
        multiplerCountry = True
    for line in open(filename):
        line = line.strip()
        if line.startswith("QSO: "):
            data = line.split()
            if len(data[1]) == 5:
                freq = data[1][:2]
            else:
                freq = data[1][:1]
            if freq not in bands:
                bands[freq] = []
                bandStates[freq] = []
                bandDXCC[freq] = []
            if (data[8]) not in bands[freq]:
                bands[freq].append(data[8])

            if not data[10].isnumeric() and not data[10] in states:
                states.append(data[10])
            elif data[10].isnumeric() and data[8] not in dxcc:
                dxcc.append(data[8])
                stn = Station(data[8])
                if stn.country not in countries:
                    countries.append(stn.country)

            if multiband:
                if not data[10].isnumeric() and not data[10] in bandStates[freq]:
                    bandStates[freq].append(data[10])
                elif data[10].isnumeric() and data[8] not in bandDXCC[freq]:
                    bandDXCC[freq].append(data[8])




    totalCalls = 0
    for callPerBand in bands.values():
        totalCalls += len(callPerBand)

    #print(totalCalls)

    if not multiband and not multiplerCountry:
        multiplier = len(states) + len(countries)
    elif not multiband and multiplerCountry:
        multiplier = len(states) + len(dxcc)

    else:
        for f in bandStates.values():
            multiplier += len(f)
        for f in bandDXCC.values():
            multiplier += len(f)

    dxcc.sort()
    states.sort()

    print("Total Score: " + str(totalCalls * multiplier) + " (" + str(totalCalls) + " * " + str(multiplier)+")")
    print("Contacts: " + str(totalCalls))
    print("Unique States: " + str(len(states)))
    print("Unique DXCC: " + str(len(dxcc)))
    print("Unique DX Countries: " + str(len(countries)))



main()