from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine, inspect, text
from django.http import HttpResponse

@csrf_exempt
def table_metadata_endpoint(request):
    if request.method == 'POST':
        #got format from sqlalchemy website
        #expected format: dialect+driver://username:password@host:port/database

        data_base_login = request.POST.get('data_base_login')

        #assumptions: I will only ever be given one DB to go through
        #DB could have multiple table or no tables
        #if no tables then simply return an empty list to represent an empty table
        #in prod I would talk to my PM about expected output in case of empty table but we are just keeping it simple to save time right now
        # each table could have many or no rows or columns
        engine = create_engine(data_base_login)
        inspector = inspect(engine)
        with engine.connect() as con:
        
            #lets grab some tables to see verify we are connecting and able to read from the DB
            tables = inspector.get_table_names()
            
            #lets build out how I will go through the DB's
            # TableMetadata = {
            # columns: List[ColumnMetadata]
            # num_rows: int
            # schema: str
            # database: str
            #}
            print(tables)
            table_metadata_list = []
            #could get it from the data_base_login but this is easier
            data_base_name = inspector.engine.url.database

            #go through the tables
            for table in tables:
                column_metadata_list = []
                columns = inspector.get_columns(table)
                #a little confused on what you would like for the schema other then a string and couldn't find anything when i google "sqlalchemy get table schema"
                #just using the table name as the schema
                data_base_schema = table

                query = 'SELECT COUNT(*) FROM ' + table
                print(query)
                #not the most afficent method but it works, I would talk to a dev who know sqlAlchemy how to do this more efficentely in prod
                row_count = con.execute(text(query)).scalar()
                #go through the columns
                for column in columns:
                    column_metadata = {
                        'col_name': column['name'],
                        'col_type': column['type'],
                    }
                    column_metadata_list.append(column_metadata)
                table_metadata = {
                    'columns': column_metadata_list,
                    'num_rows': row_count,
                    'schema': data_base_schema,
                    'database': data_base_name,
                }
                print(table_metadata)
                table_metadata_list.append(table_metadata)
            #verify everything is working and we are getting the correct data
            print(table_metadata_list)
                


        #will get to the Json response later
        return HttpResponse('helloWorld', 200)
