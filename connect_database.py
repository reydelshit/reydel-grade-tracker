import mysql.connector


class ConnectDatabase:
    def __init__(self):
        self._host = "localhost"
        self._port = 3306
        self._user = "root"
        self._password = ""
        self._database = "db_students"
        self.con = None
        self.cursor = None

    def connect_db(self):
        # Establish a database connection
        self.con = mysql.connector.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password
        )

        # Create a cursor for executing SQL queries
        self.cursor = self.con.cursor(dictionary=True)

    def add_info(self, student_id, first_name, last_name, subject, course, grade):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for adding information
        sql = f"""
            INSERT INTO students_info (studentId, firstName, lastName, subject, course, grade) 
	            VALUES ({student_id}, '{first_name}', '{last_name}', '{subject}', '{course}', '{grade}');
        """

        try:
            # Execute the SQL query for adding information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def update_info(self, student_id, first_name, last_name, subject, course, grade):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for updating information
        sql = f"""
            UPDATE students_info
                SET firstName='{first_name}', lastName='{last_name}', subject='{subject}', course='{course}', 
                    grade='{grade}'
                WHERE studentId={student_id};
        """

        try:
            # Execute the SQL query for updating information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def delete_info(self, studentId):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for deleting information
        sql = f"""  
            DELETE FROM students_info WHERE studentId={studentId};
        """

        try:
            # Execute the SQL query for deleting information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def search_info(self, student_id=None, first_name=None, last_name=None, subject=None, course=None, grade=None):
        # Connect to the database
        self.connect_db()

        condition = ""
        if student_id:
            condition += f"studentId LIKE '%{student_id}%'"
        else:
            if first_name:
                if condition:
                    condition += f" and firstName LIKE '%{first_name}%'"
                else:
                    condition += f"firstName LIKE '%{first_name}%'"

            if last_name:
                if condition:
                    condition += f" and lastName LIKE '%{last_name}%'"
                else:
                    condition += f"lastName LIKE '%{last_name}%'"

            if subject:
                if condition:
                    condition += f" and subject='{subject}'"
                else:
                    condition += f"subject='{subject}'"

            if course:
                if condition:
                    condition += f" and course='{course}'"
                else:
                    condition += f"course='{course}'"

            if grade:
                if condition:
                    condition += f" and grade LIKE '%{grade}%'"
                else:
                    condition += f"grade LIKE '%{grade}%'"

        if condition:
            # Construct SQL query for searching information with conditions
            sql = f"""
                SELECT * FROM students_info WHERE {condition};
            """
        else:
            # Construct SQL query for searching all information
            sql = f"""
                SELECT * FROM students_info;
             """

        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as E:
            return E

        finally:
            # Close the database connection
            self.con.close()

    def get_all_subjects(self):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for deleting information
        sql = f"""  
            SELECT subject FROM students_info GROUP BY subject;
        """

        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()

    def get_all_cities(self):
        # Connect to the database
        self.connect_db()

        # Construct SQL query for deleting information
        sql = f"""  
            SELECT course FROM students_info GROUP BY course;
        """

        try:
            # Execute the SQL query for searching information
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as E:
            # Rollback the transaction in case of an error
            self.con.rollback()
            return E

        finally:
            # Close the database connection
            self.con.close()
