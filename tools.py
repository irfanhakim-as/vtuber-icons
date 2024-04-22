#!/usr/bin/env python

import argparse
import json
import os

# get arguments from command line
def get_args(arguments):
    parser = argparse.ArgumentParser()
    for arg in arguments:
        if "names" in arg and "kwargs" in arg:
            parser.add_argument(*arg["names"], **arg["kwargs"])
    args, unknown = parser.parse_known_args()
    return parser, args

# read json file
def read_json(jsonFile):
    jsonDict = {}
    if os.path.isfile(jsonFile):
        with open(jsonFile, "r") as f:
            jsonDict = json.load(f)
    return jsonDict

# sort dict by keys
def sort_dict(jsonDict):
    return dict(sorted(jsonDict.items()))

# write json dict to file or stdout
def write_json(jsonDict, outFile=None):
    output = json.dumps(jsonDict, indent=4)
    if outFile:
        with open(outFile, "w") as f:
            f.write(output)
    else:
        print(output)

# get id from url
def get_id(url):
    return url.split("/")[-1]

# sort json to file
def sort_dict_to_file(args):
    # arguments = [
    #     {
    #         "names": ["--input"],
    #         "kwargs": {
    #             "help": "Input json file",
    #             "type": str,
    #             "required": True,
    #         }
    #     },
    #     {
    #         "names": ["--output"],
    #         "kwargs": {
    #             "help": "Output json file",
    #             "type": str,
    #             "default": None,
    #         }
    #     },
    # ]
    # parser, args = get_args(arguments)
    inFile = "icons.json" if not args.input else args.input
    jsonDict = read_json(inFile)
    sortedDict = sort_dict(jsonDict)
    write_json(sortedDict, args.output)

# get all icon owners
def get_owners(args):
    owners = set()
    ownersDict = {}
    # arguments = [
    #     {
    #         "names": ["--input"],
    #         "kwargs": {
    #             "help": "Input json file",
    #             "type": str,
    #             "required": True,
    #         }
    #     },
    #     {
    #         "names": ["--output"],
    #         "kwargs": {
    #             "help": "Output json file",
    #             "type": str,
    #             "default": None,
    #         }
    #     },
    # ]
    # parser, args = get_args(arguments)
    inFile = ".icons.json" if not args.input else args.input
    jsonDict = read_json(inFile)
    # jsonDict = read_json("icons.json")
    for k, v in jsonDict.items():
        for l in v:
            owners.add(l["owner"])
    for profile in owners:
        ownersDict[get_id(profile)] = profile
    sortedDict = sort_dict(ownersDict)
    write_json(sortedDict, args.output)

if __name__ == "__main__":
    choices = ["owners", "sort"]
    # get argument on which command to run
    arguments = [
        {
            "names": ["-c", "--command"],
            "kwargs": {
                "help": "command to run",
                "choices": choices,
            }
        },
    ]
    parser, args = get_args(arguments)
    # print help if command is not provided
    if args.command not in choices:
        parser.print_help()
    else:
        # get arguments for the command
        arguments = {
            "owners": [
                {
                    "names": ["--input"],
                    "kwargs": {
                        "help": "Input json file",
                        "type": str,
                        # "required": True,
                    }
                },
                {
                    "names": ["--output"],
                    "kwargs": {
                        "help": "Output json file",
                        "type": str,
                        "default": None,
                    }
                },
            ],
            "sort": [
                {
                    "names": ["--input"],
                    "kwargs": {
                        "help": "Input json file",
                        "type": str,
                        # "required": True,
                    }
                },
                {
                    "names": ["--output"],
                    "kwargs": {
                        "help": "Output json file",
                        "type": str,
                        "default": None,
                    }
                },
            ]
        }
        command = args.command
        parser, args = get_args(arguments[command])
        # run command with provided arguments
        if command == "owners":
            get_owners(args)
        elif command == "sort":
            sort_dict_to_file(args)