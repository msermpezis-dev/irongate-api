# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sqlite3

class Database:

    conn = sqlite3.connect('database/database.db', check_same_thread=False)
    c = conn.cursor()

    def get_user_id(self, email):        #returns id of email
        self.c.execute("SELECT user_id FROM UserData WHERE email = ?", (email,))
        return self.c.fetchone()[0]

    def data_entry_userdata(self, email, salt, iv, mcvalue, cvalue, emk):     #insert data into UserData table
        self.c.execute("INSERT INTO UserData (email, salt, iv, mcvalue, cvalue, emk) VALUES(?, ?, ?, ?, ?, ?)",
                  (email, salt, iv, mcvalue, cvalue, emk,))
        self.conn.commit()

    def data_entry_user_entity(self, user_id, entity_id):       #insert data into User_Entity relationship table
        self.c.execute("INSERT INTO User_Entity (user_id, entity_id) VALUES(?, ?)",
                  (user_id, entity_id,))
        self.conn.commit()

    def data_entry_entity(self, entity_name, entity_un, entity_pw, note = ''):    #insert data into Entity table and returns id of inserted entity
        self.c.execute("INSERT INTO Entity (entity_name, entity_un, entity_pw, note) VALUES(?, ?, ?, ?)",
                       (entity_name, entity_un, entity_pw, note,))
        self.conn.commit()
        return self.c.lastrowid

    def data_update_entity(self, id, eun, epw):
        self.c.execute("UPDATE Entity SET entity_un = ? WHERE entity_id = ?",
                       (eun, id))
        self.c.execute("UPDATE Entity SET entity_pw = ? WHERE entity_id = ?",
                       (epw, id))
        self.conn.commit()

    def change_pw(self, id, cvalue, emk):           #change password of current user
        self.c.execute("UPDATE UserData SET cvalue = ?, emk = ? WHERE user_id = ?", (cvalue, emk, id))
        self.conn.commit()

    def check_if_email_exists(self, email):  #returns False if user doesnt exist or the values(value,salt,iv) if user exists
        self.c.execute("SELECT count(user_id) FROM Userdata WHERE email = ?", (email,))
        n = self.c.fetchone()[0]
        if n == 0:
            return False
        else:
            return True


    def check_if_entities_exist(self, user_id):     #returns False if user has any entities and returns them if he has
        self.c.execute("SELECT count(user_id) FROM User_Entity WHERE user_id = ?", (user_id,))
        n = self.c.fetchone()[0]
        if n > 0:
            self.c.execute("SELECT Entity.entity_id, Entity.entity_name, Entity.entity_un, Entity.entity_pw, note "
                           "FROM Entity, User_Entity WHERE User_Entity.entity_id = Entity.entity_id AND user_id = ? "
                           "ORDER BY entity_name ASC", (user_id,))
            s = self.c.fetchall()
            return s
        else:
            return False

    def get_decryption_values(self, user_id):      #returns user values
        self.c.execute("SELECT user_id, salt, iv, cvalue, emk FROM UserData WHERE user_id = ?", (user_id,))
        return self.c.fetchall()[0]

    def get_decryption_values_mp(self, user_id):      #returns user values
        self.c.execute("SELECT user_id, salt, iv, cvalue, emk, mcvalue FROM UserData WHERE user_id = ?", (user_id,))
        return self.c.fetchall()[0]


    def remove_entity(self, entity_id):     #removes an entity from database
        self.c.execute("DELETE FROM User_Entity WHERE entity_id = ?", (entity_id,))
        self.c.execute("DELETE FROM Entity WHERE entity_id = ?", (entity_id,))
        self.conn.commit()

    def db_close(self):     #closes connected database
        self.c.close()
        self.conn.close()