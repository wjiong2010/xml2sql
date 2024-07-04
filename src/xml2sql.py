# ------------------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# File Name: make.py
# History maintainers:
# Maintainer: John.Wang/Ernie.Hu
# Update: 20230904
# Description: 
# ------------------------------------------------------------------------------------------------------------------------------------
import os
import sys

from xml_parser import xmlparse


class DocConverter:
    def project_type_proc(self, arg_prj_type):
        self.prj_type = arg_prj_type.lower()
        if self.prj_type != "gvxxx" and self.prj_type != "glxxx":
            raise ValueError(f"Project type {self.prj_type} not supported")

    def project_name_proc(self, arg_prj_name):
        pn = arg_prj_name
        pn_list = pn.split("_")
        if len(pn_list) > 1:
            self.prj_name = pn_list[0]
            self.cust = pn_list[1].lower()
        else:
            self.prj_name = pn
            self.cust = ""

        if pn.find("ROOT") != -1:
            self.prj_name = "ROOT"

    def __init__(self):
        self.doc_ver = ""
        self.prj_name = ""  # upper case
        self.prj_type = ""  # glxxx or gvxxx
        self.cust = ""  # mob, tza, add, geod ...
        self.cust_prefix = "custom_"
        self.DOC_DICT = {
            '<<Document Title>>': "",
            '<<Tracker Type>>': "",
            '<<Document ID>>': "",
            '<<@Track Version>>': "",
            '<<Product Image>>': "",
            '<<Status>>': ""}
        self.OPTIONS_DICT = {
            "air": "0",
            "releasenote": "1",
            "quickstart": "2",
            "usermanual": "3",
            "no_extract": "4",
            "extract_and_trans": "5",
            "debug": "6",
            "disable": "999"}
        self.pdf_password = "mospec"


dc = DocConverter()

# supported projects name
ProjectTypeID = {
    'GV305CEU': '78',
    'GV310LAU': '6E',
    'GV350CEU': '74',
    'GL33': '802002',
    'GV58CEU': '802003',
    'GV58CG': '802003',
    'GV58LAU': '802004',
    'GV355CEU': '802005',
    'GV57CG': '802006',
    'GB100CG': '802007',
    'GV50CG': '802008',
    'GV500CG': '802009',
    'GL33CG': '80200A',
    'GV75LAU': '80200C',
    'GV57CEU': '80200D',
    'GV50CME': '80200E',
    'GV50CEU': '80200F',
    'GES100CG': '802011',
    'ROOT': '802000'
}


class DocumentBuilder:
    def cut_tail(self):
        pl = os.path.split(self.d_source)
        pt = ''
        for p in pl[:-1]:  # discard the last folder
            pt = os.path.join(pt, str(p))
        self.d_source = pt
        print(os.path.dirname(self.d_source))

    def init_path(self):
        # root_path == D:\myPyFun\xml2sql
        self.root_path = os.getcwd()
        i = self.root_path.rfind('\\')
        self.root_path = self.root_path[:i]
        print(f"Root path: {self.root_path}")

        # pre_path == {root_path}\glxxx
        # pre_path == {root_path}\gvxxx\custom_mob
        low_case_prj_name = self.project_name.lower()
        if len(dc.cust) > 0:
            self.pre_path = os.path.join(dc.prj_type, dc.cust_prefix + dc.cust)

            # D:\myPyFun\xml2sql\gvxxx\custom_mob\xml\gv350ceu\GV350CEU^MOB_74_R0100_A0702_D0100_B0100_P.xml
            # D:\myPyFun\xml2sql\gvxxx\custom_mob\xml\gv350ceu\ROOT^MOB_74_R0100_A0702_D0100_B0100_P.xml
            head = f"root^{dc.cust.lower()}"
            self.r_xml = os.path.join(self.root_path, str(self.pre_path), "xml", "root",
                                      f"{head}_802000_R{self.root_ver}_A0100_D0100_B0100_P.xml")
            head = f"{self.project_name}^{dc.cust.lower()}"
            self.p_xml = os.path.join(self.root_path, str(self.pre_path), "xml", low_case_prj_name,
                                      f"{head}_{self.project_id}_R{self.root_ver}_A{self.project_ver}_D0100_B0100_P.xml")
        else:
            self.pre_path = dc.prj_type

            # D:\doc_wkspace\SW_RD\Projects\www_root\pd.queclinkhf.com\gvxxx\xml\gv57cg\GV57CG_802006_R0100_A0402_D0100_B0100_P.xml
            self.r_xml = os.path.join(self.root_path, self.pre_path, "xml", "root",
                                      f"root_802000_R{self.root_ver}_A0100_D0100_B0100_P.xml")
            self.p_xml = os.path.join(self.root_path, self.pre_path, "xml", low_case_prj_name,
                                      f"{self.project_name}_{self.project_id}_R{self.root_ver}_A{self.project_ver}_D0100_B0100_P.xml")
        print(f"pre_path: {self.pre_path}, prj_type: {dc.prj_type}")

        self.dest_folder = os.path.join(self.root_path, "excel")

    def xml_parser(self):
        if len(self.r_xml) != 0:
            xmlparse(self.r_xml)

    # ----------------------------------------------------------------------------------------------------------------------
    # python make.py <root ver>
    # python make.py <root ver> <project name> <project protocol version>
    #        argv[0]  argv[1]     argv[2]        argv[3]
    # python make.py -RV 0100 -P GV500CG -PVer 0100 -docx
    # ----------------------------------------------------------------------------------------------------------------------
    def args_parser(self, args_list):
        # print(f"args_list:{args_list}")
        arg_cnt = 0
        for arg in args_list:
            arg_value = ""
            if arg.find("=") != -1:
                t = arg.split("=")
                arg_name = t[0]
                arg_value = t[1]
            else:
                arg_name = arg
            print(f"arg_name: {arg_name}, arg_value: {arg_value}")

            match arg_name:
                case "-P":
                    # Project Name
                    arg_cnt += 1
                    # print(f"-P arg_cnt:{arg_cnt}, arg:{args_list[arg_cnt]}")
                    # self.project_name = args_list[arg_cnt].upper()
                    # dc.prj_name = self.project_name
                    dc.project_name_proc(args_list[arg_cnt].upper())
                    self.project_name = dc.prj_name
                case "-PVer":
                    # project protocol version
                    arg_cnt += 1
                    self.project_ver = args_list[arg_cnt]
                case "-PType":
                    dc.project_type_proc(arg_value)

                case "--help":
                    arg_cnt = 1
                    break
                case _:
                    arg_cnt += 1
                    continue

        if self.project_name not in ProjectTypeID.keys():
            raise ValueError(f"Wrong Project Name: {self.project_name}")

        return arg_cnt

    def show_project_info(self):
        print("Project Name: " + self.project_name + "\n"
              + "Device Type: " + self.project_id + '\n'
              + "Protocol Ver: " + self.project_ver + "\n"
              )

    def __init__(self):
        self.root_ver = '0100'
        self.d_source = None
        self.root_path = None
        self.pre_path = ""
        self.work_path = ""
        self.dest_folder = ''
        self.project_name = ""
        self.project_ver = ""
        self.project_id = ""
        self.r_xml = ""
        self.p_xml = ""
        self.work_mode = {
            # only extract root restructText.
            "root": False,
            # extract restructText of given project
            "given_project": False,
            # 5: extract_and_trans, extract rst and do docx/pdf transform,
            # 4: no_extract, do docx/pdf transform without extract rst
            # 999: disable transform, default value.
            "docx_trans": "999",
            # 0: air,
            # 1: releasenote,
            # 2: quickstart,
            # 3: usermanual
            "doc_type": "0",
            "draft": False,
            "format": ""
        }


DocBuilder = DocumentBuilder()


def create_dest_path(dbuilder=DocBuilder):
    dbuilder.init_path()
    if not os.path.exists(dbuilder.dest_folder):
        os.makedirs(dbuilder.dest_folder)
    else:
        print(dbuilder.dest_folder + ' exist!\n')


def delete_folder(folder_path):
    # traverse all the files and sub folders
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            os.remove(os.path.join(root, name))
        # for name in dirs:
        #     os.rmdir(os.path.join(root, name))
        for name in dirs:
            delete_folder(os.path.join(root, name))
    # delete the folder itself
    os.rmdir(folder_path)


# ----------------------------------------------------------------------------------------------------------------------
# python make.py <root ver>
# python make.py <root ver> <project name> <project protocol version>
#        argv[0] argv[1]  argv[2]    argv[3]    argv[4]
# python make.py -P GV500CG -PVer 0100 -PType=gvxxx
#
#        -P         : project name, GV500CG
#        -PVer      : project xml version, 0100
#        -PType     : project type, gvxxx or glxxx
# ----------------------------------------------------------------------------------------------------------------------
def main(dbuilder=DocBuilder):
    if 0 != dbuilder.args_parser(sys.argv):
        create_dest_path()

        if dbuilder.work_mode["doc_type"] == dc.OPTIONS_DICT["air"]:
            dbuilder.xml_parser()

    else:
        raise Exception("check args failed!")


if __name__ == '__main__':
    main()
