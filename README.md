# Pickle Hash Consistency Testing Tool

This tool checks how well Python's pickle works in different setups and Python versions. It helps find any  that might happen when saving and loading Python objects using different pickle formats.

## Overview

The tool tests Python's pickle serialization by:
1. Checking different data types and structures
2. Comparing hash values across environments
3. Reporting any differences found
4. Supporting pickle protocols 0 to 5

## Project Structure

```
.
├── main.py          # Main script
├── tests.py         # Test cases and hash generation functions
└── .github/         # GitHub configuration files
```

## Features

### Test Categories

1. **Simple Types**
   - Integers
   - Floating-point numbers
   - Booleans
   - Strings
   - Bytes
   - None
   - Complex numbers

2. **Complex Structures**
   - Nested lists and dictionaries
   - Tuples with various types
   - Sets and frozensets
   - Named tuples
   - DefaultDict and OrderedDict
   - Custom objects
   - Datetime objects
   - Mixed complex structures

3. **Floating Point Precision**
   - Basic arithmetic operations
   - Mathematical constants (π, e)
   - Special values (inf, -inf, NaN)
   - Very small and large numbers

4. **NumPy Special Values**
   - Infinity
   - Negative infinity
   - NaN
   - Float64 values
   - Negative zero

5. **Circular References**
   - Basic circular references
   - Nested circular references
   - Custom object circular references

## Usage

### Running Tests

```bash
python main.py --run
```

This will:
1. Run all the tests
2. Create a hash for each test result
3. Save results to a JSON file named `pickle_hash_results_{os}_{python_version}.json`

### Comparing Results

```bash
python main.py --compare [file1.json file2.json ...]
```

If no files are specified, it will compare all result files in the folder.

### Command Line Options

You can use these commands for different things:
- `--run`: Run tests and save results
- `--compare`: Compare results from specified files or all files if none specified
- `--output`: Specify output file name for test results

## Output Format

The output is a JSON file with:
- System information (OS, Python version)
- Test results for each protocol (0-5)
- Hash values for each test case

## Example Output

```json
{
  "system_info": {
    "os": "Windows",
    "python_version": "3.9.0"
  },
  "protocol_results": {
    "0": {
      "simple_types": { ... },
      "complex_structures": { ... },
      ...
    }
  }
}
```

## Comparison Report

The comparison report includes:
1. List of environments being compared
2. Detailed differences found
3. A summary of what was different
4. Notes on which protocol versions had issues

## Dependencies

- Python 3.x
- NumPy
- Standard library modules:
  - pickle
  - hashlib
  - datetime
  - collections
  - json
  - platform
  - sys

