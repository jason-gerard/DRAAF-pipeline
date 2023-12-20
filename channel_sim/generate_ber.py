import os

codecs = [
    {
        "name": "UNCODED",
        "parameters": "-K 64"
    },
    {
        "name": "REP",
        "parameters": "-N 192 -K 64"
    },
    {
        "name": "BCH",
        "parameters": "-N 31 -K 21"
    },
    {
        "name": "RS",
        "parameters": "-N 15 -K 11"
    },
    {
        "name": "TURBO",
        "parameters": "-K 64"
    },
    {
        "name": "LDPC",
        "parameters": "-N 128 -K 64 --dec-type BP_HORIZONTAL_LAYERED --dec-implem SPA -i 50 --dec-h-path conf/dec/LDPC/CCSDS_64_128.alist"
    },
]

BERs = [0.1, 0.01, 0.002, 0.001, 0.0002, 0.0001, 0.00001, 0.000001]
csv = [f",{','.join([f'{ber:.10f}' for ber in BERs])}"]

for codec in codecs:
    output_file = f"./aff3ct_outputs/{codec['name']}.txt" 
    ber_range = ",".join([f"{ber}:{ber}" for ber in BERs])
    os.system(f"/home/jason/Code/aff3ct/build/bin/aff3ct "
              f"-C \"{codec['name']}\" "
              f"{codec['parameters']} "
              f"--chn-type BSC --mdm-type OOK -R \"{ber_range}\" "
              f"-n 1000000 -e 1000000 --sim-crit-nostop "
              f"> {output_file}")

    print(codec['name'])
    row = [codec['name']]
    with open(output_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            else:
                ber = float(line.split("|")[5].strip())
                print(f'{ber:.10f}')
                row.append(f'{ber:.10f}')

    row = ",".join(row)
    csv.append(row)

with open("ber_table.csv", "w") as f:
    table = "\n".join(csv)
    f.write(table)
