# ----------------------------------------------------------------------------------------------------------------------
# File Name: regex.py
# History maintainers:
# Maintainer: John.Wang/Ernie.Hu
# Update: 20240111
# Description: compile regular expressions
# ---------------------------------------------------------------------------------------------------------------------

import re


class RegularExpression:

    def __init__(self):
        self.BOUDARY_CHECK = re.compile(r'\s*P[0-9]+\.Range\[[0-9]+]\.[LR]+\([0-9a-fA-Fglte]+\)\s*')
        # report in condition
        self.REPORT = re.compile(r'\s*#[AH]+[0-9]+\.G[0-9]+\.\s*')
        # report with double brace
        self.DB_REPORT = re.compile(r'\{\{\s*#[AH]+[0-9]+\.G[0-9]+\.\S+\s*}}')
        # random value of example in report with double brace
        self.DB_REPORT_RDV = re.compile(r'\{\{\s*#[AH]+[0-9]+\.G[0-9]+\.P[0-9-]+\.V(\.H\([0-9]\))*\s*}}')
        self.COMMAND = re.compile(r'\s*@\S+\s*')
        self.CONDITION = re.compile(r'condition\s*=\s*".+"')
        self.RANGE_BIT = re.compile(r'\s*\.P[0-9]+\.Range\.Bit\[[0-9A-Fa-f]+]')
        self.C_VALID = re.compile(r'\s*\.P[0-9]+\.C\[[0-9A-Fa-f]+\s*].valid')
        self.C_FLAG = re.compile(r'\s*\.P[0-9]+\.C\[[-,0-9A-Fa-fxX]+\s*]')
        self.C_AND_LR_FLAG = re.compile(r'^{{@[a-zA-Z]{3}.P[0-9]+\.C\[[-,0-9A-Fa-fxX]+]\|LR\[[0-9]+][+ 0-9]*\s*}}$')
        self.V_FLAG = re.compile(r'\S+\.P[0-9]+\.V')
        self.LR_FLAG = re.compile(r'\S+\.LeftRight\[[0-9]+][+ 0-9]*')
        self.MEMBER_VALID = re.compile(r'\s*\.G[0-9]+\.\[[A-Za-z]+]\.valid\s*')
        self.MEMBER_GET = re.compile(r'\s*\.G[0-9]+\.member\s*')
        self.COMMAND_NAME = re.compile(r'(?<![A-Z])[A-Z_]{3,}(?![A-Z])')
        self.ID_EQUAL = re.compile(r'id\s*=\s*"[0-9]+"')
        self.ARG_EQUAL = re.compile(r'arg[0-9]+\s*=\s*".+"')
        self.NAME_EQUAL = re.compile(r'name\s*=\s*".+"')
        self.REF_TAG = re.compile(r':ref:`[0-9a-zA-Z _:+()<>-]+`')
        self.MAIN_PATH = re.compile(r'^[a-zA-Z]+/Main$')
        self.INDEX_PATH = re.compile(r'^[a-zA-Z]+/([a-zA-Z]*/*)[a-zA-Z]+$')
        self.GROUP_PARAM_VALID = re.compile(r'\.G[0-9]+\.(?:P[0-9]+\.)*valid')
        self.GROUP_ID = re.compile(r'G[0-9]+')
        self.PARAM_ID = re.compile(r'P[0-9]+')
        self.FULL_VER = re.compile(r'(R[0-9A-F]{2})(A[0-9A-F]{2})(V[0-9A-F]{2})')
        self.C_VALID_CK = re.compile(r'\s*\.P[0-9]+\.C\[[0-9A-Fa-f]+\s*].valid\[[0-9A-Fa-f]+\s*]')