import operator


class SQLStatement:
    def create_database(self, database_name, charset='utf8'):
        pass

    def init_tables(self):
        self.tables_dict['project_table'] = ''

    def prepare_sql_statement(self):
        """
        prepare each row of table, such as parameter_table
        1. Remove identical rows
        2. convert unit string to unit id
        :return:
        """
        unique_list = []
        for lst in self.parameter_list:
            if len(lst) == 0:
                print("skip empty list")
                continue
            if len(unique_list) == 0:
                print("init list")
                unique_list.append(lst)

            exist = False
            for u_lst in unique_list:
                if operator.eq(lst, u_lst):
                    exist = True
                    break

            if not exist:
                unique_list.append(lst)

        self.parameter_list.clear()
        self.parameter_list = unique_list
        print("uniq param_lst:")
        for pl in self.parameter_list:
            print(pl)

    def get_unique_parameter_list(self):
        return self.parameter_list

    def reset(self):
        self.parameter_list.clear()

    def __init__(self):
        self.tables_dict = {}
        self.parameter_list = []


sql_statement = SQLStatement()
