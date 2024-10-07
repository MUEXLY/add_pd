import argparse
import json


def executable() -> int:

    parser = argparse.ArgumentParser(
        prog="add_pd",
        description="Add a point defect to a molecular dynamics run",
        epilog="Created and maintained by Jacob Jeffries (jwjeffr@clemson.edu, github.com/jwjeffr)"
    )
    parser.add_argument("input_file", help="Input MD run file")
    parser.add_argument("output_file", help="Output MD run file with point defect")
    parser.add_argument("defect", choices=["V", "I"], help="Defect type")
    parser.add_argument("--rmsd_cutoff", help="The RMSD cutoff for polyhedral template matching. Defaults to 0.12", type=float, default=0.12)
    parser.add_argument("--export_config_path", help="Optional configuration file specifying how the file is output.", type=str, default=None)

    args = parser.parse_args()

    from add_pd import addition

    if args.defect == "V":
        defect_type = addition.DefectType.VACANCY
    elif args.defect == "I":
        defect_type = addition.DefectType.SELF_INTERSTITIAL
    else:
        raise ValueError("invalid defect type")
    
    if args.export_config_path:
        with open(args.export_config_path, "r") as file:
            export_kwargs = json.load(file)
    else:
        export_kwargs = None

    addition.new_run(args.input_file, args.output_file, defect_type, args.rmsd_cutoff, export_kwargs=export_kwargs)

    return 0
