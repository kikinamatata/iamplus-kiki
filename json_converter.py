import json

# Step 1: Load JSON data from the file
with open('airports.json', 'r') as json_file:
    data = json.load(json_file)

def convert_airports_dictionary():
    output_file_name = 'airports_dict.json'
    output_dict = {}
    for item in data:
        iata_code = item["iata"]
        name = item["name"]
        output_dict[iata_code] = name

    with open(output_file_name, 'w') as json_file:
        json.dump(output_dict, json_file, indent=4)  # Use indent for pretty formatting
    
    print(f'Data has been written to {output_file_name}')

def convert_airports_small():   
    # Specify the output JSON file name
    output_file_name = 'airports_small.json' 
    # Step 2: Remove some values (for example, remove the "city" field from each airport entry)
    for airport in data:
        airport.pop('lon', None)
        airport.pop('iso', None)
        airport.pop('status', None)
        airport.pop('continent', None)
        airport.pop('type', None)
        airport.pop('lat', None)
        airport.pop('size', None)
    # Step 3: Save the modified data back to the file
    with open('airports_small.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f'Data has been modified and saved back to {output_file_name}')

# convert_airports_dictionary()   
convert_airports_small()