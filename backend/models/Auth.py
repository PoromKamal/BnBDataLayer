import mysql.connector
class Auth:
  mysql = mysql.connector.connect(
    host="localhost",
    user='root',
    password='admin',
    database='BnBDb'
  )

  @staticmethod
  def register_user(username, password):
    cursor = Auth.mysql.cursor()
    # Check if username already exists
    query = '''
      SELECT username
      FROM Authentication
      WHERE username = %s
    '''
    values = (username,)
    cursor.execute(query, values)
    if cursor.fetchone() is not None:
      cursor.close()
      return False
    # Insert new user
    query = '''
      INSERT INTO Authentication (username, password)
      VALUES (%s, %s)
    '''
    values = (username, password)
    cursor.execute(query, values)
    cursor.close()
    Auth.mysql.commit()
    return True