# -*- coding: utf-8 -*-

# History maintainers:
# Maintainer: John.Wang/Ernie.Hu

# import os
import re
import project as prj
import xml.dom.minidom
from xml.dom import DOMException
from regex import RegularExpression
from project import Project
import time
from sql import sql_statement as sql_stt
from database import data_base as dbs

ELEMENT_NODE = 1  # 1 is Element

regex = RegularExpression()
parsing_type = ''


# 获取 <support>
def __parse_support(node):
    for subNode in node.childNodes:
        if ELEMENT_NODE == subNode.nodeType:  # 1 is Element
            if 'S_IBattery' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.IBattery.name = tempName
                Project.Support.IBattery.valid = True
            elif 'S_LTE-Cat1' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.LTE.cat1_name = tempName
                Project.Support.LTE.cat1 = True
            elif 'S_LTE-Cat4' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.LTE.cat4_name = tempName
                Project.Support.LTE.cat4 = True
            elif 'S_2G' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.S_2G.name = tempName
                Project.Support.S_2G.valid = True
            elif 'S_3G' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.S_3G.name = tempName
                Project.Support.S_3G.valid = True
            elif 'S_BLE' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.Bluetooth.name = tempName
                Project.Support.Bluetooth.valid = True
            elif 'S_IO' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.IO.name = tempName
                Project.Support.IO.valid = True
            elif 'S_RS232' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.RS232.name = tempName
                Project.Support.RS232.valid = True
            elif 'S_RS485' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.RS485.name = tempName
                Project.Support.RS485.valid = True
            elif 'S_1-Wire' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.oneWire.name = tempName
                Project.Support.oneWire.valid = True
            elif 'S_Call' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.Call.name = tempName
                Project.Support.Call.valid = True
            elif 'S_SMS' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.SMS.name = tempName
                Project.Support.SMS.valid = True
            elif 'S_OBD' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.OBD.name = tempName
                Project.Support.OBD.valid = True
            elif 'S_CAN' == subNode.nodeName:
                Project.Support.CAN.valid = True
                hex_str = subNode.firstChild.nodeValue
                Project.Support.CAN.Mask.parse(hex_str)
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.CAN.name = tempName
            elif 'S_Tachograph' == subNode.nodeName:
                Project.Support.Tachograph.valid = True
                hex_str = subNode.firstChild.nodeValue
                Project.Support.Tachograph.Mask.parse(hex_str)
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.Tachograph.name = tempName
            elif 'S_Version' == subNode.nodeName:
                Project.Support.Versions.valid = True
                for sub in subNode.childNodes:
                    if 'Mask' == sub.nodeName:
                        hex_str = sub.firstChild.nodeValue
                        Project.Support.Versions.Mask.parse(hex_str)
            elif 'S_Format' == subNode.nodeName:
                Project.Support.Format.valid = True
                hex_str = subNode.firstChild.nodeValue
                Project.Support.Format.Mask.parse(hex_str)
            elif 'PowerButton' == subNode.nodeName:
                Project.Support.PowerButton.valid = True
            elif 'S_IP67' == subNode.nodeName:
                Project.Support.IP67.valid = True
            elif 'MBattery' == subNode.nodeName:
                tempName = subNode.getAttribute('name')
                if "" != tempName:
                    Project.Support.MBattery.name = tempName
                Project.Support.MBattery.valid = True
            elif 'Interfaces' == subNode.nodeName:
                Project.Support.Interfaces = subNode.firstChild.nodeValue
            elif 'Hardwares' == subNode.nodeName:
                Project.Support.Hardwares = subNode.firstChild.nodeValue
            elif 'Updates' == subNode.nodeName:
                Project.Support.Updates.valid = True
                for sub in subNode.childNodes:
                    if 'Mask' == sub.nodeName:
                        hex_str = sub.firstChild.nodeValue
                        Project.Support.Updates.Mask.parse(hex_str)


def __is_hex_digit(s):
    pattern = re.compile(r'^[0-9a-fA-F]+$')
    try:
        if pattern.match(s.strip()):
            return True
        else:
            return False
    except ValueError:
        print("regx no match")
        return False


# rst 文件内标签
# Get Project.AirProtocol.Commands.XXX.Px
def __parse_air_protocol_param(node, Px):
    temp_name = node.getAttribute('name')
    if node.hasChildNodes():
        for i in Px.Range.Item:
            Px.Range.Item[i].valid = False
        Px.Range.clear_items()
        Px.Range.clear_leftright()
    # temp_name = node.getAttribute('name')
    if "" != temp_name:
        Px.name = temp_name
        print("----------{0}---------\r\n".format(Px.name))
    if Px.name.upper() != "RESERVED":
        desc = ''
        unit_id = 0
        value_format = 0
        for sub in node.childNodes:
            # print(sub.nodeName + '\n')
            if 'Len' == sub.nodeName:
                Px.Len = sub.firstChild.nodeValue
            if 'Default' == sub.nodeName:
                Px.Default = sub.firstChild.nodeValue
            if 'Range' == sub.nodeName:
                if sub.hasAttribute('type'):
                    range_type = sub.getAttribute('type')
                    if range_type in Px.Range.RangeType:
                        Px.Range.rng_type = range_type
                        # print(range_type + " : " + Px.Range.rng_type + "\n")
                    else:
                        raise Exception('The Range type ' + str(range_type) + ' is not supported now.')
                if sub.hasAttribute('filter'):
                    filter_mask = sub.getAttribute('filter')
                    # print(f"filter_mask: {filter_mask}")
                    Px.Range.filter_mask.parse(filter_mask)

                if sub.hasAttribute('unit'):
                    # print(f"filter_mask: {filter_mask}")
                    Px.Range.unit = sub.getAttribute('unit')
                    unit_id = dbs.get_unit_table_id(Px.Range.unit)

                Px.Range.Items = ''
                Px.Range.ItemCnt = 0
                t_lr = Px.Range._LeftRight()

                for sub2 in sub.childNodes:
                    # print("sub2 in sub.childNodes" + sub2.nodeName + '\n')
                    if 'Item' == sub2.nodeName:
                        value = sub2.firstChild.nodeValue
                        name = sub2.getAttribute('name')
                        model = sub2.getAttribute('model')

                        if "hexNumber" == Px.Range.rng_type and __is_hex_digit(value):
                            hex_int_v = int(value, 16)
                            # print("-----hex_int_v-" + str(hex_int_v))
                            if hex_int_v not in Px.Range.Item:
                                Px.Range.Item[hex_int_v] = prj.IDc()
                            Px.Range.Item[hex_int_v].name = name
                            Px.Range.Item[hex_int_v].valid = True
                            vv = hex_int_v
                            value_format = 1
                            if len(name) != 0:
                                desc += "{:x}:{}".format(hex_int_v, name)
                        elif value.isdigit():
                            # print("digital value: {}".format(value))
                            if int(value) not in Px.Range.Item:
                                Px.Range.Item[int(value)] = prj.IDc()
                            Px.Range.Item[int(value)].name = name
                            Px.Range.Item[int(value)].valid = True
                            vv = int(value)
                            value_format = 2
                            Px.Range.rng_type = "digital_deci"  # decimal
                            if len(name) != 0:
                                desc += "|{}:{}".format(vv, name)
                        else:
                            print("not digital value: {} {}".format(name, value))
                            if value not in Px.Range.Item:
                                Px.Range.Item[value] = prj.IDc()
                            Px.Range.Item[value].name = name
                            Px.Range.Item[value].valid = True
                            vv = value
                            value_format = 0
                            Px.Range.rng_type = "special_str"

                        if len(model) != 0:
                            Px.Range.Item[vv].model_list = model.split(',')
                            # print(f"str(model) = {model}, vv = {vv}, model_list={str(Px.Range.Item[vv].model_list)}")

                        Px.Range.Items += value + ', '
                        Px.Range.add_item(value)
                        Px.Range.ItemCnt += 1
                        # print("cnt:{0}, items_list:{1}, items:{2}".format(Px.Range.ItemCnt, str(Px.Range.items_list),
                        #                                                   Px.Range.Items))
                    if 'Left' == sub2.nodeName:
                        t_lr.l = sub2.firstChild.nodeValue
                    if 'Right' == sub2.nodeName:
                        t_lr.r = sub2.firstChild.nodeValue
                        Px.Range.add_leftright(t_lr)
                        # print("left: {0}, right: {1}".format(t_lr.l, t_lr.r))

        lr_str = Px.Range.get_leftright()
        items_str = Px.Range.get_items_str()
        print("para_name:<{}> L:{} D:{} F:{}, lr:{}, items:{}, U:{}, desc:{}".format(Px.name, Px.Len, Px.Default, Px.Range.filter_mask.value, lr_str, items_str, unit_id, desc))

        p_list = [Px.name, Px.Len, items_str.strip(), lr_str, Px.Default, value_format, Px.Range.filter_mask.value, 0, unit_id, 1]
        sql_stt.parameter_list.append(p_list)

        Px.valid = True


# Get Project.AirProtocol.Commands.XXX
def __parse_air_protocol_cmd(node, cmd, name=''):
    c = 0
    # print("--------------{0}--------------".format(name))
    for sub in node.childNodes:
        c += 1
        # if re.match(r"P[0-9]", sub.nodeName):
        if regex.PARAM_ID.match(sub.nodeName):
            __parse_air_protocol_param(sub, eval("cmd." + sub.nodeName))

    cmd.valid = True
    cmd.name = name
    cmd.param_count = c


# Get Project.AirProtocol.Commands
def __parse_air_protocol_commands(node):
    c = 0
    pri_fix = "Project.AirProtocol.Commands."
    for sub in node.childNodes:
        c += 1
        # command name must consist of three capital letters.
        # that is what the regular expression means
        # if re.match(r"(?<![A-Z])[A-Z]{3}(?![A-Z])", sub.nodeName):
        if regex.COMMAND_NAME.match(sub.nodeName):
            __parse_air_protocol_cmd(sub, eval(pri_fix + sub.nodeName), sub.nodeName)

    Project.AirProtocol.Commands.cmd_count = c


# get attribute of node,
def __parse_attr(node, attr):
    value = node.getAttribute(attr)
    # not found will trigger exception, 'element xxx has no attributes.'
    if "" == value:
        raise Exception('Element \'' + node.nodeName + '\' has no \'' + attr + '\' attribute.')
    return value


def __parse_air_protocol_group(node, group_x):
    global parsing_type
    group_x.member_clear()
    group_x.member = ''
    group_x.valid = False
    if node.hasAttribute('member'):
        group_x.member = node.getAttribute('member')
        temp_list = group_x.member.split('|')
        for tl in temp_list:
            group_x.member_list.append(tl.strip())
        group_x.valid = True
        print("++++++{0}++{1}++++++++++".format(parsing_type, group_x.member))
        for n in node.childNodes:
            # if re.match(r"P[0-9]+", n.nodeName):
            if regex.PARAM_ID.match(n.nodeName):
                __parse_air_protocol_param(n, eval("group_x." + n.nodeName))

    else:
        print("{0} don't have name".format(node.nodeName))


def __parse_air_protocol_ascii(node):
    # print("parse ascii report")
    Project.AirProtocol.Ascii.valid = True
    pre_fix = "Project.AirProtocol.Ascii."
    # print(str(node.name))
    for sub in node.childNodes:
        # print("subNode name: {0}".format(sub.nodeName))
        match sub.nodeName:
            case 'POSI':
                Project.AirProtocol.Ascii.posi.valid = True
                mtype = "posi."
            case 'DINF':
                Project.AirProtocol.Ascii.dinf.valid = True
                mtype = "dinf."
            case 'RTRP':
                Project.AirProtocol.Ascii.rtrp.valid = True
                mtype = "rtrp."
            case 'EVNT':
                Project.AirProtocol.Ascii.event.valid = True
                mtype = "event."
            case 'DATA':
                Project.AirProtocol.Ascii.data.valid = True
                mtype = "data."
            case 'CDATA':
                Project.AirProtocol.Ascii.crash.valid = True
                mtype = "crash."
            case 'CINF':
                Project.AirProtocol.Ascii.cinf.valid = True
                mtype = "cinf."
            case 'UPDR':
                Project.AirProtocol.Ascii.updr.valid = True
                mtype = "updr."
            case 'CONR':
                Project.AirProtocol.Ascii.conr.valid = True
                mtype = "conr."
            case _:
                continue

        for sub2 in sub.childNodes:
            if regex.GROUP_ID.match(sub2.nodeName):
                __parse_air_protocol_group(sub2, eval(pre_fix + mtype + sub2.nodeName))


def __parse_air_protocol_hex(node):
    # print("parse hex report")
    Project.AirProtocol.Hex.valid = True
    pre_fix = "Project.AirProtocol.Hex."
    for sub in node.childNodes:
        # print("subNode name: {0}".format(sub.nodeName))
        # mtype = ''
        match sub.nodeName:
            case 'POSI':
                Project.AirProtocol.Hex.posi.valid = True
                mtype = "posi."
            case 'DINF':
                Project.AirProtocol.Hex.dinf.valid = True
                mtype = "dinf."
            # case 'RTRP':
            #     Project.AirProtocol.Hex.rtrp.valid = True
            #     mtype = "rtrp."
            case 'EVNT':
                Project.AirProtocol.Hex.event.valid = True
                mtype = "event."
            case 'DATA':
                Project.AirProtocol.Hex.data.valid = True
                mtype = "data."
            case 'CDATA':
                Project.AirProtocol.Hex.crash.valid = True
                mtype = "crash."
            case 'CINF':
                Project.AirProtocol.Hex.cinf.valid = True
                mtype = "cinf."
            # case 'UPDR':
            #     Project.AirProtocol.Hex.updr.valid = True
            #     mtype = "updr."
            case 'CONR':
                Project.AirProtocol.Hex.conr.valid = True
                mtype = "conr."
            case _:
                continue

        for sub2 in sub.childNodes:
            if regex.GROUP_ID.match(sub2.nodeName):
                __parse_air_protocol_group(sub2, eval(pre_fix + mtype + sub2.nodeName))


def __parse_air_protocol(node):
    global parsing_type
    Project.AirProtocol.ver = __parse_attr(node, 'ver')
    for sub_node in node.childNodes:
        if ELEMENT_NODE == sub_node.nodeType:  # 1 is Element
            parsing_type = sub_node.nodeName
            if 'Commands' == sub_node.nodeName:
                __parse_air_protocol_commands(sub_node)
            elif 'Ascii' == sub_node.nodeName:
                __parse_air_protocol_ascii(sub_node)
            elif 'Hex' == sub_node.nodeName:
                __parse_air_protocol_hex(sub_node)
    Project.AirProtocol.valid = True


def xmlparse_f(file):
    try:
        dom = xml.dom.minidom.parse(file)
    except DOMException:
        raise Exception(file + ' is NOT a well-formed XML file.')

    root = dom.documentElement

    if root.nodeName != 'Project':
        raise Exception('XML has no \'Project\' element.')

    # Get attributes of Project
    Project.root = __parse_attr(root, 'root')
    Project.name = __parse_attr(root, 'name')
    Project.device_type = __parse_attr(root, 'device_type')
    Project.password = __parse_attr(root, 'password')
    Project.sub_title = __parse_attr(root, 'sub_title')
    Project.qldbg = __parse_attr(root, 'qldbg')
    Project.qble = __parse_attr(root, 'qble')

    for node in root.childNodes:
        if ELEMENT_NODE == node.nodeType:  # 1 is Element
            if 'Support' == node.nodeName:
                __parse_support(node)
            elif 'AirProtocol' == node.nodeName:
                __parse_air_protocol(node)


def valid2false():
    Project.Support.reset()
    Project.AirProtocol.Ascii.reset()
    Project.AirProtocol.Hex.reset()
    Project.AirProtocol.Commands.reset()


def xmlparse(file):
    time.process_time()
    valid2false()
    xmlparse_f(file)
    print('Successfully parsed the XML file. Cost {:9.9} seconds!'.format(time.process_time()))

# xmlparse()
