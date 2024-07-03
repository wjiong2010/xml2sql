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
import shutil

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

    def copy_draft(self):
        self._dft = os.path.join(os.getcwd(), "draft", "root")
        print(f"Copying draft, {self._dft}, to {self._rel_dft}")
        if os.path.exists(self._rel_dft):
            delete_folder(self._rel_dft)
        # os.mkdir(self._rel_dft)
        shutil.copytree(self._dft, self._rel_dft)

    def xml_parser(self, t=0):
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
        get_prj_name = False
        get_prj_ver = False
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
                case "-draft":
                    self.work_mode["draft"] = True
                case "-RV":
                    # Root xml version
                    arg_cnt += 1
                    # print(f"-RV arg_cnt:{arg_cnt}, arg:{args_list[arg_cnt]}")
                    self.work_mode["root"] = True
                    self.root_ver = args_list[arg_cnt]
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
                    # print("-PVer")
                    get_prj_ver = True
                    self.project_ver = args_list[arg_cnt]
                case "-PType":
                    dc.project_type_proc(arg_value)
                case "-DVer":
                    # project protocol version
                    arg_cnt += 1
                    print(f"-DVer, {args_list[arg_cnt]}")
                    self.doc_ver = args_list[arg_cnt]
                    dc.doc_ver = self.doc_ver
                case "-docx":
                    # Enable docx convert:
                    # no_extract
                    # extract_and_trans(default)
                    if arg_value != "":
                        self.work_mode["docx_trans"] = dc.OPTIONS_DICT[arg_value]
                    else:
                        self.work_mode["docx_trans"] = dc.OPTIONS_DICT["extract_and_trans"]
                case "-format":
                    # html(default), docx, pdf, all
                    # if -type is quickstart or usermanual, only pdf is supported
                    if arg_value != "":
                        self.work_mode["format"] = arg_value
                    else:
                        self.work_mode["format"] = "html"
                case "-type":
                    # 0: air(default), 1: releasenote, 2:quickstart, 3:usermanual
                    _doc_type = args_list[arg_cnt]
                    if arg_value != "":
                        self.work_mode["doc_type"] = dc.OPTIONS_DICT[arg_value]
                    if self.work_mode["doc_type"] == dc.OPTIONS_DICT["quickstart"]:
                        self.doc_ver = "0100"
                        dc.doc_ver = self.doc_ver
                case "--help":
                    arg_cnt = 0
                    break
                case _:
                    arg_cnt += 1
                    continue

        if (self.work_mode["doc_type"] != dc.OPTIONS_DICT["quickstart"] and
                self.work_mode["doc_type"] != dc.OPTIONS_DICT["usermanual"] and self.project_name != ""):
            self.project_id = ProjectTypeID[self.project_name]
            get_prj_name = True
            if self.project_name not in ProjectTypeID.keys():
                raise ValueError(f"Wrong Project Name: {self.project_name}")

        if get_prj_ver and get_prj_name:
            self.work_mode["given_project"] = True

        if self.project_name.lower() == 'root':
            self.work_mode["format"] = "html"

        return 0

    def show_project_info(self):
        print("Root Protocol Ver: " + self.root_ver + "\n"
              + "Project Name: " + self.project_name + "\n"
              + "Device Type: " + self.project_id + '\n'
              + "Protocol Ver: " + self.project_ver + "\n"
              )

    def __init__(self):
        self._r = 'release'
        self._a = 'air'
        self._rn = 'releasenote'
        self._u = 'usermanual'
        self._q = 'quickstart'
        self._s = 'source'
        self._dft = os.path.join("draft", "root")
        self._rel_dft = os.path.join("release", "root_draft")
        self.pre_path = ""
        self.d_source = ''
        self.work_path = ""
        self.dest_folder = ''
        self.project_name = ""
        self.project_ver = ""
        self.project_id = ""
        self.root_ver = "0100"
        self.root_path = ""
        self.doc_ver = ""
        self.root_xml = ""
        self.project_xml = ""
        self.latex_folder = ""
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
    if not os.path.exists(dbuilder.d_source):
        os.makedirs(dbuilder.d_source)
    else:
        print(dbuilder.d_source + ' exist!\n')


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
# python make.py -RV 0100 -P GV500CG -PVer 0100 -type=air/releasenote/quickstart/usermanual -draft
#
#        -RV        : root xml version, such as: 0100
#        -P         : project name, GV500CG
#        -PVer      : project xml version, 0100
#        -PType     : project type, gvxxx or glxxx
#        -DVer      : document version, 0100
#        -docx      : no_extract
#                   : extract_and_trans
#        -format    : docx, pdf, html, all
#        -type      : air
#                   : releasenote
#                   : quickstart
#                   : usermanual
#        -draft     : only copy draft/root to release/root_draft   (OBSOLETE)
# ----------------------------------------------------------------------------------------------------------------------
def main(dbuilder=DocBuilder):
    if 0 != dbuilder.args_parser(sys.argv):
        create_dest_path()

        if dbuilder.work_mode["doc_type"] == dc.OPTIONS_DICT["air"]:
            dbuilder.xml_parser(dbuilder.work_mode["doc_type"])

    else:
        raise Exception("check args failed!")


if __name__ == '__main__':
    main()
