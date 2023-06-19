import contextlib
import csv
import os
import sqlite3

from os.path import exists


class InvestmentCalculator:
    def __init__(self):
        self.state = 0

    def show_main_menu(self):
        print('''MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria''')

    def show_crud_menu(self):
        print('''CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies''')

    def show_top_ten_menu(self):
        print('''TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA''')

    def get_input(self):
        print()
        return input('Enter an option:')

    def create_company(self):
        ticker = input("Enter ticker (in the format 'MOON'):")
        company = input("Enter company (in the format 'Moon Corp'):")
        industries = input("Enter industries (in the format 'Technology'):")
        ebitda = int(input("Enter ebitda (in the format '987654321'):"))
        sales = int(input("Enter sales (in the format '987654321'):"))
        net_profit = int(input("Enter net profit (in the format '987654321'):"))
        market_price = int(input("Enter market price (in the format '987654321'):"))
        net_dept = int(input("Enter net debt (in the format '987654321'):"))
        assets = int(input("Enter assets (in the format '987654321'):"))
        equity = int(input("Enter equity (in the format '987654321'):"))
        cash_equiv = int(input("Enter cash equivalents (in the format '987654321'):"))
        liabilities = int(input("Enter liabilities (in the format '987654321'):"))
        row_company = (ticker, company, industries)
        row_financial = (ticker, ebitda, sales, net_profit,
                         market_price, net_dept, assets,
                         equity, cash_equiv, liabilities)
        self.insert_into_table("companies", row_company)
        self.insert_into_table("financial", row_financial)
        print("Company created successfully!")

    def handle_division_from_db_cursor_data(self, cursor):
        rows = cursor.fetchall()

        if rows and rows[0][0] and rows[0][1]:
            result = float(rows[0][0]) / float(rows[0][1])
            return round(result, 2)
        else:
            return None

    # P/E = Market price / Net profit
    def get_p_e(self, cursor, ticker):
        cursor.execute(f"SELECT market_price, net_profit FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # P/S = Market price / Sales
    def get_p_s(self, cursor, ticker):
        cursor.execute(f"SELECT market_price, sales FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # P/B = Market price / Assets
    def get_p_b(self, cursor, ticker):
        cursor.execute(f"SELECT market_price, assets FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # ND/EBITDA = Net debt / EBITDA
    def get_nd_ebitda(self, cursor, ticker):
        cursor.execute(f"SELECT net_debt, ebitda FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # ROE = Net profit / Equity
    def get_roe(self, cursor, ticker):
        cursor.execute(f"SELECT net_profit, equity FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # ROA = Net profit / Assets
    def get_roa(self, cursor, ticker):
        cursor.execute(f"SELECT net_profit, assets FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    # L/A = Liabilities / Assets
    def get_l_a(self, cursor, ticker):
        cursor.execute(f"SELECT liabilities, assets FROM financial WHERE ticker LIKE '%{ticker}%';")
        return self.handle_division_from_db_cursor_data(cursor)

    def read_company(self):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            name_part = input('Enter company name:')

            cursor.execute(f"SELECT name, ticker FROM companies WHERE name LIKE '%{name_part}%';")

            rows = cursor.fetchall()

            if not rows:
                print('Company not found!')
                print()
                return

            for idx, row in enumerate(rows):
                print(idx, row[0])

            number = int(input('Enter company number:'))
            ticker = rows[number][1]
            name = rows[number][0]
            print(f'{ticker} {name}')
            print(f'P/E = {self.get_p_e(cursor, ticker)}')
            print(f'P/S = {self.get_p_s(cursor, ticker)}')
            print(f'P/B = {self.get_p_b(cursor, ticker)}')
            print(f'ND/EBITDA = {self.get_nd_ebitda(cursor, ticker)}')
            print(f'ROE = {self.get_roe(cursor, ticker)}')
            print(f'ROA = {self.get_roa(cursor, ticker)}')
            print(f'L/A = {self.get_l_a(cursor, ticker)}')
            print()
            cursor.close()

    def update_company(self):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            name_part = input('Enter company name:')

            cursor.execute(f"SELECT name, ticker FROM companies WHERE name LIKE '%{name_part}%';")

            rows = cursor.fetchall()

            if not rows:
                print('Company not found!')
                print()
                return

            for idx, row in enumerate(rows):
                print(idx, row[0])

            number = int(input('Enter company number:'))
            ticker = rows[number][1]

            ebitda = int(input("Enter ebitda (in the format '987654321'):"))
            sales = int(input("Enter sales (in the format '987654321'):"))
            net_profit = int(input("Enter net profit (in the format '987654321'):"))
            market_price = int(input("Enter market price (in the format '987654321'):"))
            net_debt = int(input("Enter net debt (in the format '987654321'):"))
            assets = int(input("Enter assets (in the format '987654321'):"))
            equity = int(input("Enter equity (in the format '987654321'):"))
            cash_equivalents = int(input("Enter cash equivalents (in the format '987654321'):"))
            liabilities = int(input("Enter liabilities (in the format '987654321'):"))

            update_query = "UPDATE financial SET ebitda = ?, sales = ?," + \
                           " net_profit = ?, market_price = ?, net_debt = ?," + \
                           " assets = ?, equity = ?, cash_equivalents = ?," + \
                           " liabilities = ? WHERE ticker = ?;"
            data = (ebitda, sales, net_profit, market_price, net_debt,
                    assets, equity, cash_equivalents, liabilities, ticker)

            cursor.execute(update_query, data)
            con.commit()
            print('Company updated successfully!')
            cursor.close()

    def delete_company(self):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            name_part = input('Enter company name:')

            cursor.execute(f"SELECT name, ticker FROM companies WHERE name LIKE '%{name_part}%';")

            rows = cursor.fetchall()

            if not rows:
                print('Company not found!')
                print()
                return

            for idx, row in enumerate(rows):
                print(idx, row[0])

            number = int(input('Enter company number:'))
            ticker = rows[number][1]

            delete_financial_query = "DELETE FROM financial WHERE ticker = ?;"
            delete_companies_query = "DELETE FROM companies WHERE ticker = ?;"
            data = (ticker,)

            cursor.execute(delete_financial_query, data)
            con.commit()
            cursor.execute(delete_companies_query, data)
            con.commit()
            print('Company deleted successfully!')
            cursor.close()

    def list_companies(self):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            companies_list = []

            cursor.execute(f"SELECT ticker, name, sector FROM companies ORDER BY ticker;")

            rows = cursor.fetchall()

            for idx, row in enumerate(rows):
                company = ' '.join(row)
                companies_list.append(company)

            print('COMPANY LIST')
            for company in companies_list:
                print(company)
            cursor.close()

    def handle_equal_ticker_case_list(self, financial_list):
        reverse_financial_dict = {}
        for row in financial_list:
            ticker, value = row.split(' ')
            if value not in reverse_financial_dict:
                reverse_financial_dict[value] = list()
            reverse_financial_dict[value].append(ticker)

        reverse_financial_dict = {key: sorted(value, reverse=(len(value) > 2)) for key, value in
                                  reverse_financial_dict.items()}
        key_list = list(reverse_financial_dict.keys())
        key_list = sorted(key_list, reverse=True)
        new_financial_list = []
        for key in key_list:
            for value in reverse_financial_dict[key]:
                new_financial_list.append(f'{value} {key}')
        return new_financial_list

    def handle_list_top_ratio(self, query, message_title, size=10):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            financial_list = []

            cursor.execute(query)

            rows = cursor.fetchall()

            for idx, row in enumerate(rows):
                if row[1] is None:
                    continue

                ratio = float(row[1])
                financial = row[0] + ' ' + str(ratio)
                financial_list.append(financial)

            cursor.close()

            financial_list = sorted(financial_list,
                                    key=lambda x: x.split(' ')[1],
                                    reverse=True)[:size]
            financial_list = self.handle_equal_ticker_case_list(financial_list)

            print(message_title)
            for financial in financial_list:
                print(financial)
            print()

    def list_top_nd_ebitda(self, size=10):
        query = "SELECT ticker, ROUND(net_debt / ebitda, 2) FROM financial ORDER BY ticker;"
        message_title = 'TICKER ND/EBITDA'
        self.handle_list_top_ratio(query, message_title)

    def list_top_roe(self, size=10):
        query = "SELECT ticker, ROUND(net_profit / equity, 2) FROM financial ORDER BY ticker;"
        message_title = 'TICKER ROE'
        self.handle_list_top_ratio(query, message_title)

    def list_top_roa(self, size=10):
        query = "SELECT ticker, ROUND(net_profit / assets, 2) FROM financial ORDER BY ticker;"
        message_title = 'TICKER ROA'
        self.handle_list_top_ratio(query, message_title)

    def process_main_menu(self):
        while True:
            if self.state == 0:
                self.show_main_menu()
                choice = self.get_input()
                if choice not in ('0', '1', '2'):
                    print('Invalid option!')
                else:
                    choice = int(choice)
                    if choice == 0:
                        print('Have a nice day!')
                        break
                    else:
                        self.state = choice
            elif self.state == 1:
                self.show_crud_menu()
                choice = self.get_input()
                if not choice.isdigit() or int(choice) not in range(6):
                    print('Invalid option!')
                else:
                    choice = int(choice)
                    if choice > 5:
                        print('Not implemented!')
                    elif choice == 1:
                        self.create_company()
                    elif choice == 2:
                        self.read_company()
                    elif choice == 3:
                        self.update_company()
                    elif choice == 4:
                        self.delete_company()
                    elif choice == 5:
                        self.list_companies()
                print()
                self.state = 0
            elif self.state == 2:
                self.show_top_ten_menu()
                choice = self.get_input()
                if not choice.isdigit() or int(choice) not in range(4):
                    print('Invalid option!')
                elif int(choice) == 1:
                    self.list_top_nd_ebitda()
                elif int(choice) == 2:
                    self.list_top_roe()
                elif int(choice) == 3:
                    self.list_top_roa()
                elif int(choice) > 3:
                    print('Not implemented!')
                self.state = 0

    def process_lst_elem(self, elem):
        if elem == '':
            return None

        return elem

    def read_csv_data(self):
        companies_filename = 'test/companies.csv'
        companies_list = []
        with open(companies_filename, 'r') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=",")  # Create a reader object
            for line in file_reader:  # Read each line
                new_line = [self.process_lst_elem(el) for el in line]
                companies_list.append(new_line)

        financial_filename = 'test/financial.csv'
        financial_list = []
        with open(financial_filename, 'r') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=",")  # Create a reader object
            for line in file_reader:  # Read each line
                new_line = [self.process_lst_elem(el) for el in line]
                financial_list.append(new_line)

        return companies_list[1:], financial_list[1:]

    def insert_into_table(self, table, data):
        with contextlib.closing(sqlite3.connect('investor.db')) as con:
            cursor = con.cursor()
            # insert a row in the specified table
            cursor.execute(f"INSERT INTO {table} VALUES({str('?, ' * len(data))[:-2]});",
                           data)

            con.commit()
            cursor.close()

    def process_database(self):
        if not exists('investor.db'):
            with contextlib.closing(sqlite3.connect('investor.db')) as con:
                cursor = con.cursor()
                # create the companies table
                cursor.execute("""CREATE TABLE IF NOT EXISTS companies(
                    ticker TEXT PRIMARY KEY,
                    name TEXT,
                    sector TEXT
                    );""")

                # create the financial table
                cursor.execute("""CREATE TABLE IF NOT EXISTS financial(
                      ticker TEXT PRIMARY KEY,
                      ebitda REAL,
                      sales REAL,
                      net_profit REAL,
                      market_price REAL,
                      net_debt REAL,
                      assets REAL,
                      equity REAL,
                      cash_equivalents REAL,
                      liabilities REAL
                      );""")

                con.commit()

                companies_list, financial_list = self.read_csv_data()

                cursor.executemany("INSERT INTO companies VALUES (?, ?, ?)", companies_list)
                con.commit()  # saves the changes

                cursor.executemany("INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   financial_list)
                con.commit()
                cursor.close()


if __name__ == "__main__":
    calc = InvestmentCalculator()
    calc.process_database()
    print('Welcome to the Investor Program!')
    calc.process_main_menu()
