import flask
import logging
import mysql.connector
import sys


# Initialize
logging.basicConfig( stream=sys.stdout, level=logging.DEBUG, format='%(filename)s %(funcName)s():  %(message)s' )
logging.warning( f'starting' )
app = flask.Flask( __name__ )


# Webpage handlers
@app.get('/')
def main_page( ):
    http_request = flask.request
    http_response = flask.make_response()
    set_standard_headers( http_response )
    logging.warning( f'main_page() http_request={http_request}' )

    database_connection, database_cursor = initialize_database()
    pages_served = increment_pages_served( database_connection, database_cursor )

    template_values = { 'site_name':'Minimal Docker + Flask + Mysql', 'pages_served':pages_served }
    http_response.data = flask.render_template( 'main.html', **template_values )
    return http_response


def initialize_database( ):
    # Read database password from secret file
    database_password = None
    with open( '/run/secrets/database_password' ) as password_in:
        database_password = password_in.read().strip()

    # Connect to database
    database_connection = mysql.connector.connect(
        host='example-database', database='my_web_app', user='my_web_app_user', password=database_password, auth_plugin='mysql_native_password' )
    database_cursor = database_connection.cursor()

    # Ensure table exists
    database_cursor.execute( " create table if not exists my_table ( name varchar(64) primary key not null, counter int not null ) " )
    return database_connection, database_cursor


def increment_pages_served( database_connection, database_cursor ):
    # Increment counter
    database_cursor.execute( " insert into my_table ( name, counter ) values ( 'page', 1 )  on duplicate key update counter = counter + 1 " )
    database_connection.commit()

    # Get current counter value
    database_cursor.execute( " select name, counter from my_table where name='page' " )
    ( name, counter ) = database_cursor.fetchone()
    logging.warning( f'increment_pages_served() name={name} counter={counter}' )
    return counter


def set_standard_headers( http_response ):
    http_response.headers['X-Frame-Options'] = 'deny'
    http_response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"


# Entry point
if __name__ == '__main__':
    app.run( host='0.0.0.0' )  # Serve on all IP addresses


