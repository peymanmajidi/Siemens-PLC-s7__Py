def Logo():
    with open('./Modules/logo.txt', 'r') as file:
        data = file.read()
        print(data)

def Init():
    print("""
┌───────┬──────────────────┬─────────────────────────┬──────────────┬───────────────────────┐
│  #    │       CITY       │          BARCODE        │     GATE     │      TIME STAMP       │
├───────┼──────────────────┼─────────────────────────┼──────────────┼───────────────────────┤
└───────┴──────────────────┴─────────────────────────┴──────────────┴───────────────────────┘\r""",end = '')

def Print_Row(i,gate, city, barcode, sortTime):
    gate_str = str(gate) if gate >9 else "0" + str(gate)
    row = f"│  #    │       CITY       │          BARCODE        │     GATE     │      TIME STAMP       │"
    row = row[:2] + str(i) + ((5-len(str(i)))* ' ') + row[7:]
    row = row[:10] + city + ((17 - len(city))* ' ') + row[27:]
    row = row[:30] + barcode + ((22 - len(barcode))* ' ') + row[52:]
    row = row[:59] + gate_str + ((8 - len(gate_str))* ' ') + row[67:]
    row = row[:71] + sortTime + ((21 - len(sortTime))* ' ') + row[92:]
    print(row)
    print("└───────┴──────────────────┴─────────────────────────┴──────────────┴───────────────────────┘\r",end = '')
