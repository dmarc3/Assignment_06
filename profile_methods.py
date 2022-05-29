from cProfile import Profile
import ipdb
import Assignment_03.main as main3
import Assignment_03.socialnetwork_model as sn3
import Assignment_05.main as main5
import Assignment_05.socialnetwork_db as sn5


def reset_databases():
    ''' Method to remove data in databases '''
    # Assignment 03 Database
    user_collection3 = main3.init_user_collection()
    if user_collection3.database.table_exists():
        user_collection3.database.drop_table()
    status_collection3 = main3.init_status_collection()
    if status_collection3.database.table_exists():
        status_collection3.database.drop_table()
    sn3.db.create_tables([sn3.Users, sn3.Status])
    # Assignment 05 Database
    # with sn5.MongoDBConnection() as mongo:
    #     user_collection5 = main5.init_user_collection(mongo)
    #     user_collection5.database.drop()
    #     status_collection5 = main5.init_status_collection(mongo)
    #     status_collection5.database.drop()

def time_load_status_updates(filename: str) -> bool:
    ''' Test load status method '''
    # with Profile() as pr:
    #     result = main3.load_status_updates(filename, status_collection3)
    #     ipdb.set_trace()
    #     assert result == True
    # ipdb.set_trace()
    pass

if __name__ == '__main__':
    # Reset databases
    reset_databases()
    # Initialize new collecitons
    user_collection3 = main3.init_user_collection()
    status_collection3 = main3.init_status_collection()
    with sn5.MongoDBConnection() as mongo:
        user_collection5 = main5.init_user_collection(mongo)
        status_collection5 = main5.init_status_collection(mongo)
    
    # time_load_users
    result = main3.load_users('accounts.csv', user_collection3)
    assert result == True
    # time_load_status_updates
    result = main3.load_status_updates('status_updates.csv', status_collection3)
    assert result == True