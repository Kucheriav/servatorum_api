from fastapi import FastAPI
from app.routers import user_routes
from app.db_management import init_db


# init_db()
app = FastAPI()
app.include_router(user_routes.router, prefix="/users", tags=["users"])




#
# {'project': [{'alembic':'содержимое папки alembic'},
#              {'app':[
#                  {'crud':['__init__.py', 'user_crud.py']},
#                  {'models':['__init__.py','user.py']},
#                  {'routers':['user_routers.py']},
#                  {'schemas':['__init__.py', 'user.py']},
#                  {'test_scripts':['create_user_request_test.py']},
#                  'database.py',
#                  'main.py'
#              ]},
#              'alembic.ini',
#             'examples.py',
#              'requirements.txt'
#              ]
# }