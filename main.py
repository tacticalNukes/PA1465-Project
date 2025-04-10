import argparse
import glob
import json
import platform
import sys

from code import test_simple_types, test_complex_structures, test_circular_references, test_numpy_special_values, \
    test_floating_point_precision


def run_tests():
    # System information
    system_info = {
        "os": platform.system(),
        "python_version": sys.version.split()[0]
    }

    protocol_results = {}

    # RUn through all protocols and test results
    for i in range(6):
        print(f"Testing Protocol {i}:")
        protocol_results[i] = {
            "simple_types": test_simple_types(i),
            "complex_structures": test_complex_structures(i),
            "floating_point_precision": test_floating_point_precision(i),
            "numpy_special_values": test_numpy_special_values(i),
            "circular_references": test_circular_references(i)
        }

    return {
        "system_info": system_info,
        "protocol_results": protocol_results
    }


def save_results(results, filename=None):
    """Save test results to a JSON file."""
    if filename is None:
        os_name = results["system_info"]["os"].lower()
        py_version = results["system_info"]["python_version"]
        filename = f"pickle_hash_results_{os_name}_py{py_version}.json"

    with open(filename, 'w') as f:
        # Convert defaultdict to dict for JSON serialization
        json.dump(results, f, indent=2)

    print(f"Results saved to {filename}")
    return filename


def compare_results(file_paths=None):
    """Compare results from different test runs."""
    # If no files specified, use all JSON files in the current directory
    if file_paths is None:
        file_paths = glob.glob("pickle_hash_results_*.json")
        if not file_paths:
            print("No result files found for comparison")
            return

    # Load all result files
    all_results = []
    for path in file_paths:
        try:
            with open(path, 'r') as f:
                results = json.load(f)
            all_results.append(results)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading {path}: {e}")

    if len(all_results) < 2:
        print("Need at least two result sets to compare")
        return

    # Create a system identifier for each result set
    system_ids = []
    for results in all_results:
        info = results["system_info"]
        system_id = f"{info['os']} {info['python_version']}"
        system_ids.append(system_id)

    # Compare results
    differences = {}

    # Use the first result as a reference
    reference = all_results[0]
    reference_id = system_ids[0]

    # For each protocol
    for protocol in reference["protocol_results"]:
        protocol_diffs = {}

        # For each test type (simple, complex)
        for test_type in reference["protocol_results"][protocol]:
            type_diffs = {}
            ref_tests = reference["protocol_results"][protocol][test_type]

            # For each specific test
            for test_name, ref_hash in ref_tests.items():
                # Compare with other result sets
                for i, other_results in enumerate(all_results[1:], 1):
                    if (protocol in other_results["protocol_results"] and
                            test_type in other_results["protocol_results"][protocol] and
                            test_name in other_results["protocol_results"][protocol][test_type]):

                        other_hash = other_results["protocol_results"][protocol][test_type][test_name]
                        if ref_hash != other_hash:
                            if test_name not in type_diffs:
                                type_diffs[test_name] = {}

                            type_diffs[test_name][system_ids[i]] = {
                                "reference": ref_hash,
                                "other": other_hash
                            }

            if type_diffs:
                protocol_diffs[test_type] = type_diffs

        if protocol_diffs:
            differences[f"Protocol {protocol}"] = protocol_diffs

    # Generate report
    print("\n===== COMPARISON REPORT =====\n")

    if not differences:
        print("All hash values are identical across all tested environments!")
    else:
        print(f"Reference environment: {reference_id}")
        print(f"Comparing against: {', '.join(system_ids[1:])}")
        print(f"Found differences in {len(differences)} protocols\n")

        for protocol, protocol_diffs in differences.items():
            print(f"\n{protocol}:")

            for test_type, type_diffs in protocol_diffs.items():
                print(f"  {test_type}:")

                for test_name, envs in type_diffs.items():
                    print(f"    {test_name}:")
                    for env, hashes in envs.items():
                        print(f"      {env}: {hashes['other']}")
                        print(f"      {reference_id}: {hashes['reference']}")
                        print()

    # Create a summary table
    print("\n===== SUMMARY =====\n")

    # Count differences by environment
    env_diff_counts = {env: 0 for env in system_ids[1:]}

    for protocol_diffs in differences.values():
        for type_diffs in protocol_diffs.values():
            for test_diffs in type_diffs.values():
                for env in test_diffs:
                    env_diff_counts[env] += 1

    # Print counts
    for env, count in env_diff_counts.items():
        print(f"{env} differs from {reference_id} in {count} tests")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test pickle hash consistency across environments")
    parser.add_argument("--run", action="store_true", help="Run tests and save results")
    parser.add_argument("--compare", nargs='*',
                        help="Compare results from specified files or all files if none specified")
    parser.add_argument("--output", help="Output file name for test results")

    args = parser.parse_args()

    if args.run:
        results = run_tests()
        save_results(results, args.output)

    if args.compare is not None:
        if args.compare:
            compare_results(args.compare)
        else:
            compare_results()
    if not (args.run or args.compare is not None):
        parser.print_help()
