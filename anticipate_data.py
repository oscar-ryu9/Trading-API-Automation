# Initialize total profit/loss
total = 0
symbols = ["PLTR", "INTC", "PLUG", "RKLB", "PCG", "UPWK", "SNAP", "LYFT", "STNE", "SOFI", "HOOD", "QS"]
# symbols = ["QS"]
my_list = []

for symbol in symbols:
    filename = "April_Test/" + symbol + ".txt"
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into its components
            parts = line.split()
            my_list.append(parts)

    for i in range(len(my_list)):
        if my_list[i] == [symbol]:
            if my_list[i+3] == []:
                pricing = float(my_list[i+1][1]) * float(my_list[i+2][0])
                if my_list[i+1][0] == "SELL,":
                    total += pricing
                else:
                    total -= pricing
            else:
                pricing1 = float(my_list[i+1][1]) * float(my_list[i+3][0])
                pricing2 = float(my_list[i+2][1]) * float(my_list[i+3][0])
                if my_list[i+1][0] == "SELL,":
                    total += pricing1
                    if my_list[i+2][0] == "SELL,":
                        total += pricing2
                    else:
                        total -= pricing2
                else:
                    total -= pricing1
                    if my_list[i+2][0] == "SELL,":
                        total += pricing2
                    else:
                        total -= pricing2


print(total)
