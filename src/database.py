import os
import openpyxl
from excel_format import ExcelFormat
from project import Project

xl_format = ExcelFormat()


class Tables:
    def __init__(self):
        self.name = ''
        self.headline = []


class ProjectTables(Tables):
    def get_value(self, prj):

        if Project.Support.LTE.cat1:
            self.lte = Project.Support.LTE.cat1_name
        if Project.Support.LTE.cat4:
            self.lte = Project.Support.LTE.cat4_name

        if Project.Support.CAN.valid:
            if Project.Support.CAN.Mask.Bit[0].value == '1':
                self.can = "CAN100"
            if Project.Support.CAN.Mask.Bit[1].value == '1':
                self.can = "CANModule"
        else:
            self.can = 'NS'

        if Project.Support.Tachograph.valid:
            if Project.Support.Tachograph.Mask.Bit[0].value == '1':
                self.tacho = "THR100"
            if Project.Support.Tachograph.Mask.Bit[1].value == '1':
                self.tacho = "Tachograph"
        else:
            self.tacho = 'NS'

        if Project.Support.IP67.valid:
            self.waterproof = 'IP67'
        else:
            self.waterproof = 'IPxx'

        cust = prj.customer
        if prj.customer == '':
            cust = 'standard'

        row = [prj.name, prj.root, str(prj.AirProtocol.ver), cust, prj.qldbg, prj.qble, prj.device_type,
               prj.password, prj.sub_title, self.lte, prj.Support.S_3G.valid, prj.Support.S_2G.valid, prj.Support.Bluetooth.valid,
               prj.Support.RS232.valid, prj.Support.RS485.valid, self.can, self.tacho, prj.Support.OBD.valid,
               prj.Support.IO.valid, prj.Support.Call.valid, prj.Support.SMS.valid, self.waterproof,
               Project.Support.Versions.Mask.Bits, Project.Support.Format.Mask.Bits, Project.Support.IBattery.valid]
        print(str(row))

        return row

    def __init__(self):
        super().__init__()
        self.lte = ''
        self.can = ''
        self.tacho = ''
        self.waterproof = ''
        self.name = 'project_table'
        self.headline = \
            ['name', 'root_version', 'protocol_version', 'customer', 'qldbg', 'qble', 'device_type', 'password',
             'sub_title', 'cell_4g', 'cell_3g', 'cell_2g', 'ble', 'rs232', 'rs485', 'can', 'tachograph', 'obd', 'io',
             'phone_call', 'sms', 'waterproof', 'version', 'message_format', 'inner_battery']


class DataBase:
    def __init__(self):
        self.COL_A_WIDTH = 20
        self.COL_B_WIDTH = 120
        self.tables_dict = {
            "project_table": ProjectTables()
        }

    def get_project_value(self, table_name, first_line, prj=Project):
        table = self.tables_dict[table_name]
        if first_line:
            return table.headline
        else:
            return table.get_value(prj)

    def build_excel_table(self, ws, r):
        print(f"{str(r)} next line----------------------------")
        ori_r = r
        rc = f"A{r}"
        print(f"{rc}")
        ws[rc] = f"{self.name_cn}({self.name_en})".title()
        mg_rc = f"A{r}:B{r}"
        ws.merge_cells(mg_rc)
        xl_format.set_cell(ws[rc], font=xl_format.cell_title_font)
        rc = f"B{r}"
        xl_format.set_cell(ws[rc], font=xl_format.cell_title_font)

        for cr in self.cr_result:
            r += 1
            r0 = r
            rc = f"A{r}"
            ws[rc] = cr.severity.upper()
            print(f"{rc}, {cr.severity.upper()}")
            xl_format.set_cell(ws[rc])

            rc = f"B{r}"
            lines = 0
            rc_str = f"{cr.msg}"
            lines += 1
            if len(cr.msg) != len(cr.verbose):
                rc_str += '\n'
                rc_str += f"{cr.verbose}"
                lines += len(cr.verbose) / Team().COL_B_WIDTH + 1
                print("lines: " + str(lines))
            ws[rc] = rc_str
            xl_format.set_cell(ws[rc])
            xl_format.set_row(ws, r, 15 * lines + 10)
            print(f"{rc}, {rc_str}, {cr.verbose}")

            r += 1
            rc = f"B{r}"
            rc_str = ''
            lines = 0
            for location in cr.locations:
                if lines > 0:
                    rc_str += '\n'
                if len(cr.locations) == 1:
                    rc_str += f"{cr.id}:"
                else:
                    rc_str += f"{location.info}:"
                rc_str += '\n'
                lines += 1
                l = f"{location.filename} line:{location.line}, col:{location.column}"
                rc_str += l
                lines += len(l) / Team().COL_B_WIDTH + 1
            ws[rc] = rc_str
            xl_format.set_cell(ws[rc])
            xl_format.set_row(ws, r, 15 * lines + 10)
            print(f"{rc}, {ws[rc]}")

            r += 1
            rc = f"B{r}"
            ws[rc] = f"修复结果："
            xl_format.set_cell(ws[rc])

            mg_rc = f"A{r0}:A{r}"
            ws.merge_cells(mg_rc)

        return r - ori_r


data_base = DataBase()


def save_as_excel(dest_path, file_name, sheet_name, db=data_base):
    excel_full_path = str(os.path.join(dest_path, file_name))

    # wb = Workbook()
    # ws_app = wb.active
    # ws_app.title = sheet_name
    # ws_sys = wb.create_sheet("System")
    try:
        wb = openpyxl.load_workbook(excel_full_path)
    except FileNotFoundError:
        wb = openpyxl.Workbook()

    try:
        ws = wb[sheet_name]
    except KeyError:
        ws = wb.active
        ws.title = sheet_name

    # 获得最大行数
    max_row_num = ws.max_row
    # 获得最大列数
    max_col_num = ws.max_column
    # 将当前行设置为最大行数
    ws._current_row = max_row_num
    print(f"max_row_num: {max_row_num}, max_col_num: {max_col_num}, sheet_name: {sheet_name}")

    # 使用append方法，将行数据按行追加写入
    if max_row_num == 1:
        values = db.get_project_value(sheet_name, True)
        ws.append(values)
    values = db.get_project_value(sheet_name, False)
    ws.append(values)

    # xl_format.set_column(ws_app, 'A', self.COL_A_WIDTH)
    # xl_format.set_column(ws_app, 'B', self.COL_B_WIDTH)

    # Save the file
    wb.save(excel_full_path)
