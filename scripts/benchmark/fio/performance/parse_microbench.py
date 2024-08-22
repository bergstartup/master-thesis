import json
import re
import numpy as np
import sys

# Define the input and output file paths
input_file = "op"
output_file = "output.json"

target_pid = int(sys.argv[1])
print("The target pid is", target_pid)

# Regular expression pattern to match each microbench line
pattern = r"@microbench\[(\d+)\,(\d+)\]: \((\d+), (\d+), (\d+), (\d+), (\d+)\)"

# Dictionary to hold the parsed data
microbench_data = {}
end_to_end_values = []

# Open and read the input file
with open(input_file, "r") as file:
    for line in file:
        # Use regex to find matches
        match = re.match(pattern, line)
        if match:
            key = match.group(2)
            pid = int(match.group(1))
            
            # Check if the pid matches the target pid
            if pid != target_pid:
                continue

            # Create a dictionary for the tuple values
            values = {
                "block": int(match.group(2)),
                "nvmeof_initiator": int(match.group(3)),
                "tcp": int(match.group(4)),
                "target": int(match.group(5)),
                "end_to_end": int(match.group(6))
            }
            # Add the entry to the microbench_data dictionary
            microbench_data[key] = values

            # Collect the end-to-end value for percentile calculation
            end_to_end_values.append(values["end_to_end"])


# Calculate the 99th percentile of the 'end_to_end' key
percentile_99 = np.percentile(end_to_end_values, 99)

# Write the parsed data to the JSON output file
with open(output_file, "w") as json_file:
    json.dump(microbench_data, json_file, indent=4)


print(f"99th percentile of 'end_to_end' values: {percentile_99}")
print(f"JSON output written to {output_file}")

