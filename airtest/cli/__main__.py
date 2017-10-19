# -*- coding: utf-8 -*-
from airtest.cli.parser import get_parser


def main():
    ap = get_parser()
    args = ap.parse_args()
    if args.action == "info":
        from airtest.cli.info import get_script_info
        print(get_script_info(args.script))
    elif args.action == "report":
        from airtest.report.report import main as report_main
        report_main(args)
    elif args.action == "run":
        from airtest.cli.runner import run_script
        run_script(args)


if __name__ == '__main__':
    main()
