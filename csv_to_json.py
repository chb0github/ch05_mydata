#!/usr/bin/env python3
import csv
import json
import sys
import argparse

def trim_value(val):
    if val is None:
        return None
    return val.strip()

def convert_value(val):
    # Early exits for None/empty
    if val is None:
        return None

    if isinstance(val, list):
        val = ",".join(str(v) for v in val)

    val = val.strip()
    if not val:
        return None

    # Quick check: first char must look numeric
    if val[0] not in '-+0123456789.':
        return val

    # Try conversions
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        return val

def pivot_data(rows, fieldnames):
    data = {}
    if fieldnames:
        # Standardize fieldnames to strings
        keys = [str(f) for f in fieldnames]
        
        # Check if any row has extra columns (None key in DictReader)
        for row in rows:
            if None in row and "None" not in keys:
                keys.append("None")
                
        for key in keys:
            data[key] = []
        
        for row in rows:
            # Map the row keys to strings
            row_data = {str(k): v for k, v in row.items()}
            for key in keys:
                val = row_data.get(key)
                data[key].append(convert_value(val))
    return data

def csv_to_json(input_stream, output_stream, pivot=False):
    reader = csv.DictReader(input_stream, skipinitialspace=True)
    fieldnames = reader.fieldnames
    rows = list(reader)
    
    if pivot:
        data = pivot_data(rows, fieldnames)
    else:
        data = []
        for row in rows:
            converted_row = {str(k): convert_value(v) for k, v in row.items()}
            data.append(converted_row)
            
    json.dump(data, output_stream, indent=4)
    output_stream.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV to JSON with optional pivoting.")
    parser.add_argument("-i", "--input", type=str, help="Path to the input CSV file (default: stdin)")
    parser.add_argument("-o", "--output", type=str, help="Path to the output JSON file (default: stdout)")
    parser.add_argument("--pivot", action="store_true", help="Pivot the output JSON")
    
    args = parser.parse_args()
    
    input_stream = sys.stdin
    output_stream = sys.stdout
    
    try:
        if args.input:
            input_stream = open(args.input, 'r', encoding='utf-8')
        
        if args.output:
            output_stream = open(args.output, 'w', encoding='utf-8')
            
        csv_to_json(input_stream, output_stream, pivot=args.pivot)

            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if input_stream is not sys.stdin:
            input_stream.close()
        if output_stream is not sys.stdout:
            output_stream.close()
