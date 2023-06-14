from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine, inspect
from django.http import HttpResponse

@csrf_exempt
def table_metadata_endpoint(request):
    if request.method == 'POST':
        #got format from sqlalchemy website
        #expected format: dialect+driver://username:password@host:port/database
        data_base_login = request.POST.get('data_base_login')

        #lets connect now!
        print(data_base_login)
        engine = create_engine(data_base_login)
        inspector = inspect(engine)
        #lets grab some tables to see verify we are connecting and able to read from the DB
        tables = inspector.get_table_names()
        print(tables)
        #looks good!

        return HttpResponse('helloWorld', 200)
