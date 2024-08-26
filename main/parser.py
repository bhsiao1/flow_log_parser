import csv

# Main function to run the defined methods to get a output file.
def main():
    flow_log_file = 'main/flow_log.txt'
    lookup_table_file = 'main/lookup_table.csv'
    
    lookup_table = convert_lookup_table(lookup_table_file)

    result = map_flow_log(flow_log_file, lookup_table)

    convert_output_to_file(result)

# Convert output (dictionary) to comma separated values in a plain text file
def convert_output_to_file(result):
    lines = []
    for key, val in result.items():
        if isinstance(key, tuple):
            key = ",".join(key)
        
        line = key + "," + str(val)
        lines.append(line)

    sorted_lines = sorted(lines, key = lambda x: len(x.split(",")))

    with open("main/output.txt", mode='w') as file:
        for line in sorted_lines:
            file.write(line + '\n')

# Grab flow log data and get the respective tag for it (or unnamed)
def map_flow_log(log_file, lookup_table):
    # Can manually add conversions for now
    protocol_dict = {"1": "icmp", "2": "igmp", "6": "tcp", "17": "udp"}
    output = {}
    with open(log_file, mode='r') as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            fields = line.split()

            dstport = fields[5]
            protocol_num = fields[7]
            protocol = protocol_dict.get(protocol_num)
            tag = lookup_table.get((dstport, protocol), "Untagged")
            output[tag] = output.get(tag, 0) + 1
            output[(dstport, protocol)] = output.get((dstport, protocol), 0) + 1
    return output

# Convert lookup table to a dictionary of (dstport, protocol) key to a tag value.
def convert_lookup_table(lookup_csv):
    lookup_table = {}
    with open(lookup_csv, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            dstport = row['dstport']
            protocol = row['protocol']
            tag = row['tag']

            lookup_table[(dstport, protocol)] = tag

    return lookup_table

if __name__ == "__main__":
    main()