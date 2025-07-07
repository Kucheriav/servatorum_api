# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import database_exists, create_database, drop_database
#
#
# def recreate_db():
#     engine = create_engine('postgresql://gleb:postgres@localhost:5432/servatorium_test_db')
#     drop_database(engine.url)
#     engine = None
#     engine = create_engine('postgresql://gleb:postgres@localhost:5432/servatorium_test_db')



from fastapi import Depends

@router.post("/patch_user/{user_id}")
async def patch_user(user_id: int, ..., user=Depends(get_current_user)):
    ...

# или целиком для всех ручек в роутере
user_router = APIRouter(dependencies=[Depends(get_current_user)])