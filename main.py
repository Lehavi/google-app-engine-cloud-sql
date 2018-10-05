import os
import MySQLdb
import webapp2

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        db = connect_to_cloudsql()
        cursor = db.cursor()

        s = """
		select
		psid,
		name
		from
		pm_core.song
		where
		psid < %(psid)s
		"""
        cursor.execute(s, { 'psid': 1000 })

        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))

# This is what executes from app.yaml for any HTML handler
# MAIN
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
			
# Connection to Cloud SQL, using parameters that app.yaml loads into the env
def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # Or connect to a local MYSQL server using TCP
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

