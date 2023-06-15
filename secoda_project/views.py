from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine, inspect
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
        #lets grab some tables to see verify we are connecting and able to read from the DB
        tables = inspector.get_table_names()
        
        #lets build out how I will go through the DB's
        # TableMetadata = {
        # columns: List[ColumnMetadata]
        # num_rows: int
        # schema: str
        # database: str
        #}

        table_metadata = []

        #go through the tables
        for table in tables:
            column_metadata = []
            # ColumnMetadata = {
                # col_name: str
                # col_type: str
                # }
            #go through the columns
            for column in columns:
                


        #will get to the Json response later
        return HttpResponse('helloWorld', 200)
