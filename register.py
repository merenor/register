#import yaml
import time
import sqlite3
from collections import OrderedDict
import locale

class Register():
    content = {}
    file_loaded = False
    conn = None


    def add_item(self, name, page):
        if self.conn:
            cur = self.conn.cursor()

            # check if name exists already in table names
            cur.execute("SELECT id,name FROM names WHERE name='{name}';".format(name=name))
            current_name = cur.fetchone()

            if not current_name:
                print("Name neu. Füge hinzu ...")
                # Insert new name, id is automatically given
                cur.execute("INSERT INTO names (NAME) VALUES ('{name}');".format(name=name))
                self.conn.commit()

                # Select name from db to get name AND id
                cur.execute("SELECT id,name FROM names WHERE name='{name}';".format(name=name))
                current_name = cur.fetchone()

            # Problem: no page entrys for "voir"!
            elif 'voir' in current_name[1]:
                print("FEHLER: Kann nicht zu VOIR-Eintrag hinzufügen.")
                return False

            # Insert new pair of name-id and page into pages-tab
            # Check if entry already exists
            cur.execute("""SELECT name_id, page FROM pages
                WHERE name_id='{name_id}' AND page='{page}';""".format(
                    name_id = current_name[0],
                    page = page))
            if cur.fetchone():
                print("Eintrag existiert schon auf der Seite.")
                return False
            else:
                cur.execute("""INSERT INTO pages (NAME_ID, PAGE)
                    VALUES ('{name_id}', '{page}');""".format(
                        name_id = current_name[0],
                        page = page))
                self.conn.commit()
            return True

    def add_item_by_id(self, id, page):
        if self.conn:

            cur = self.conn.cursor()

            # Does ID exist in names table?
            cur.execute("""SELECT name,id FROM names
                WHERE id='{id}';""".format(id = id))
            if not cur.fetchone():
                print("ID nicht gefunden.")
                return False

            # Does ID,page entry already exist?
            cur.execute("""SELECT name_id, page FROM pages
                WHERE name_id='{name_id}' AND page='{page}';""".format(
                    name_id = id,
                    page = page))
            if cur.fetchone():
                print("Eintrag existiert schon auf der Seite.")
                return False
            else:
                cur.execute("""INSERT INTO pages (NAME_ID, PAGE)
                    VALUES ('{name_id}', '{page}');""".format(
                        name_id = id,
                        page = page))
                self.conn.commit()
            return True


    def get_pages_by_name(self, name):
        pages_list = []

        if self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT id,name FROM names WHERE name='{name}';".format(name=name))
            current_name = cur.fetchone()

            if current_name:
                cur.execute("""SELECT page FROM pages
                    WHERE NAME_ID='{name_id}'""".format(
                        name_id=current_name[0]))

                all_rows = cur.fetchall()
                for row in all_rows:
                    pages_list.append(int(row[0]))
                pages_list.sort()

        return pages_list


    def get_pages_by_name_id(self, name_id):
        pages_list = []

        if self.conn:
            cur = self.conn.cursor()

            cur.execute("""SELECT page FROM pages
                WHERE NAME_ID='{name_id}'""".format(
                name_id=name_id))

            all_rows = cur.fetchall()
            for row in all_rows:
                pages_list.append(int(row[0]))
            pages_list.sort()

            return pages_list


    def get_name_by_id(self, id):
        if self.conn:

            cur = self.conn.cursor()

            cur.execute("SELECT id,name FROM names WHERE id='{id}';".format(id=id))
            return cur.fetchone()


    def find_name(self, name):
        cur = self.conn.cursor()

        cur.execute("SELECT id,name FROM names WHERE name LIKE '%{name}%';".format(name=name))
        return cur.fetchall()


    def get_all_names(self):
        if self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT id,name FROM names ORDER BY name COLLATE french;")
            return cur.fetchall()


    def clear(self):
        pass

    def find(self, search):
        pass

    def save_to_yaml(self, filename):
        content = OrderedDict(sorted(self.content.items()))

        with open(filename, 'w') as f:
            f.write(yaml.dump(content))

        # Save also a backup file
        file, ext = filename.rsplit('.', 1)
        backup = '{beginning}_backup_{time}.{ending}'.format(
            beginning = file,
            time = time.strftime("%Y-%m-%d_%H-%M-%S"),
            ending = ext)

        with open(backup, 'w') as g:
            g.write(yaml.dump(content))


    def load_from_yaml(self, filename):
        with open(filename, 'r') as f:
            file_content = f.read()
        self.content = yaml.load(file_content)

        self.file_loaded = True


    def create(self, filename):
        self.conn = sqlite3.connect(filename)

        # Table names
        self.conn.execute('DROP TABLE IF EXISTS names;')
        self.conn.execute('''CREATE TABLE names
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            VOIR INT);''')

        # Table pages
        self.conn.execute('DROP TABLE IF EXISTS pages;')
        self.conn.execute('''CREATE TABLE pages
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME_ID INT NOT NULL,
            PAGE TEXT NOT NULL);''')
        self.conn.commit()


    def del_name(self, id):
        if self.conn:
            cur = self.conn.cursor()

            cur.execute("DELETE FROM names WHERE ID='{id}';".format(id=id))
            self.conn.commit()


    def del_page(self, name_id, page):
        if self.conn:
            cur = self.conn.cursor()

            cur.execute("DELETE FROM pages WHERE NAME_ID='{name_id}' AND PAGE='{page}';".format(name_id=name_id, page=page))
            self.conn.commit()

    def get_names(self, page):
        names_list = []

        if self.conn:
            cur = self.conn.cursor()

            cur.execute("SELECT name_id, page FROM pages WHERE page='{page}'".format(page=page))
            all_rows = cur.fetchall()

            for row in all_rows:
                cur.execute("SELECT name from names WHERE id='{id}'".format(id=row[0]))
                name = cur.fetchone()
                if name:
                    names_list.append(name[0])

        return names_list


    def load(self, filename):
        # important for sorting the french accents
        locale.setlocale(locale.LC_ALL, 'fr')

        self.conn = sqlite3.connect(filename)

        # method for sorting the french way
        self.conn.create_collation("french", locale.strcoll)


    def is_loaded(self):
        return self.conn


    def close(self):
        if self.conn:
            self.conn.close()


    def import_names(self, filename):
        names = []
        counter = 0

        if self.conn:
            cur = self.conn.cursor()

            # read names from a vorlaufregister-file
            with open(filename, 'r', encoding="utf-8") as f:
                for line in f:
                    if '  ' in line:
                        try:
                            name,pages = line.split("  ", 1)
                        except:
                            print("FEHLER bei Trennung von {}".format(line))
                    else:
                        name = line
                    names.append(name.strip())
                    counter = counter + 1

            # add them to the database
            for name in names:

                print("Bearbeite {} ...".format(name))
                # check if name exists already in table names
                cur.execute("SELECT id,name FROM names WHERE name='{name}';".format(name=name))
                current_name = cur.fetchone()

                if not current_name:
                    # Insert new name, id is automatically given
                    cur.execute("INSERT INTO names (NAME) VALUES ('{name}');".format(name=name))
                    self.conn.commit()

                else:
                    print("Name '{}' existiert schon mit ID {}.".format(current_name[1], current_name[0]))

            print("{} Einträge hinzugefügt.".format(counter))


    def rename(self, old_name_id, new_name):

        if self.conn:

            cur = self.conn.cursor()
            # get the name entry
            cur.execute("SELECT id,name FROM names WHERE id='{old_name_id}';".format(old_name_id=old_name_id))
            current_name = cur.fetchone()

            # if exists, update it to new name
            if current_name:
                cur.execute("""UPDATE names SET name='{new_name}'
                    WHERE id='{old_name_id}'""".format(
                        new_name=new_name,
                        old_name_id=old_name_id))


    def __str__(self):
        return "Register object"
