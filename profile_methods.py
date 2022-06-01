'''
Profiling Assignment_03 and Assignment_05.
Kathleen Wong focused on profiling Assignment_03 and peewee implementation.
Marcus Bakke focused on profiling Assignment_05 and MongoDB implementation.
'''
from timeit import default_timer as timer
import Assignment_03.main as main3
import Assignment_03.socialnetwork_model as sn3
import Assignment_05.main as main5
import Assignment_05.socialnetwork_db as sn5

NUM = 5


def reset_databases(typ: int):
    ''' Method to remove data in databases '''
    if typ == 0:
        del_users = True
        del_status = True
    elif typ == 1:
        del_users = True
        del_status = False
    elif typ == 2:
        del_users = False
        del_status = True
    # Assignment 03 Database
    if del_users:
        main3.init_user_collection()
        if sn3.Users.table_exists():
            sn3.Users.drop_table()
            sn3.db.create_tables([sn3.Users])
    if del_status:
        main3.init_status_collection()
        if sn3.Status.table_exists():
            sn3.Status.delete().execute()
            # sn3.Status.drop_table()
            # sn3.db.create_tables([sn3.Status])
    # Assignment 05 Database
    if del_users:
        with sn5.MongoDBConnection() as mongo:
            user_collection5 = main5.init_user_collection(mongo)
            user_collection5.database.drop()
    if del_status:
        with sn5.MongoDBConnection() as mongo:
            status_collection5 = main5.init_status_collection(mongo)
            status_collection5.database.drop()


def time_load_users(filename: str) -> bool:
    ''' Test load accounts method '''
    time3 = 0
    user_collection3 = main3.init_user_collection()
    for i in range(NUM):
        print(f'  Loading {filename} via Assignment_03 for time_load_users... {i+1}')
        start = timer()
        result = main3.load_users(filename, user_collection3)
        end = timer()
        if result:
            if end - start > time3:
                time3 = end - start
            reset_databases(1)

    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Loading {filename} via Assignment_05... {i+1}')
            start = timer()
            result = main5.load_users(filename, main5.init_user_collection(mongo))
            end = timer()
            # assert result == True
            if end - start > time5:
                time5 = end - start
            reset_databases(1)

    return time3, time5


def time_load_status_updates(filename: str) -> bool:
    ''' Test load status method '''
    reset_databases(2)
    time3 = 0
    status_collection3 = main3.init_status_collection()
    for i in range(NUM):
        print(f'  Loading {filename} via Assignment_03 for time_load_status_updates... {i+1}')
        start = timer()
        result = main3.load_status_updates(filename, status_collection3)
        end = timer()
        if result:
            if end - start > time3:
                time3 = end - start
        reset_databases(2)

    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Loading {filename} via Assignment_05 for time_load_status_updates... {i+1}')
            start = timer()
            result = main5.load_status_updates(filename, main5.init_status_collection(mongo))
            end = timer()
            # assert result == True
            if end - start > time5:
                time5 = end - start
            reset_databases(2)
    return time3, time5


def time_add_user(user_id: str, email: str, user_name: str, user_last_name: str) -> bool:
    ''' Test add user method '''
    time3 = 0
    user_collection3 = main3.init_user_collection()
    for i in range(NUM):
        print(f'  Adding user via Assignment_05... {i+1}')
        start = timer()
        result = main3.add_user(user_id,
                                email,
                                user_name,
                                user_last_name,
                                user_collection3)
        end = timer()
        if result:
            if end - start > time3:
                time3 = end - start
            result = main3.delete_user(user_id, user_collection3)
            if result:
                pass
        reset_databases(1)

    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Adding user via Assignment_05... {i+1}')
            start = timer()
            result = main5.add_user(user_id,
                                    email,
                                    user_name,
                                    user_last_name,
                                    main5.init_user_collection(mongo))
            end = timer()
            if result.acknowledged:
                if end - start > time5:
                    time5 = end - start
                result = main5.delete_user(user_id,
                                           main5.init_user_collection(mongo))
                if result:
                    pass

    return time3, time5


def time_add_status(user_id: str, status_id: str, status_text: str) -> bool:
    ''' Test load status method '''
    time3 = 0
    status_collection3 = main3.init_status_collection()
    for i in range(NUM):
        print(f'  Adding status via Assignment_03... {i+1}')
        start = timer()
        result = main3.add_status(user_id,
                                  status_id,
                                  status_text,
                                  status_collection3)
        end = timer()
        if result:
            if end - start > time3:
                time3 = end - start
            result = main5.delete_status(status_id,
                                         status_collection3)
            if result:
                reset_databases(3)
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Adding status via Assignment_05... {i+1}')
            start = timer()
            result = main5.add_status(user_id,
                                      status_id,
                                      status_text,
                                      main5.init_status_collection(mongo))
            end = timer()
            if result.acknowledged:
                if end - start > time5:
                    time5 = end - start
                result = main5.delete_status(status_id,
                                             main5.init_status_collection(mongo))
                if result:
                    pass

    return time3, time5


def print_times(time_list: list):
    ''' Print profile results '''
    print()
    print('          Assignment_03  Assignment_05')
    print('          -------------  -------------')
    print('Results:  '+'{0:.8f}'.format(time_list[0]).rjust(13) + \
          '  '+'{0:.8f}'.format(time_list[1]).rjust(13))
    print('\n')


if __name__ == '__main__':
    print(f'\nNUM set to: {NUM}')

    # Reset databases
    # reset_databases(0)

    # Final results dictionary
    results = {'load_users': '',
               'load_status_updates': '',
               'add_user': '',
               'add_status': ''}

    # # time_load_users
    # print('\n'+'Timing load_users for Assignment #3 and #5:')
    # print('-------------------------------------------')
    # times = time_load_users('accounts.csv')
    # print_times(times)
    # results['load_users'] = times

    # time_load_status_updates
    print('\n'+'Timing load_status_updates for Assignment #3 and #5:')
    print('----------------------------------------------------')
    times = time_load_status_updates('status_updates.csv')
    print_times(times)
    results['load_status_updates'] = times

    # # time_add_user
    # print('\n'+'Timing add_user for Assignment #3 and #5:')
    # print('-----------------------------------------')
    # times = time_add_user('test123',
    #                       'test@gmail.com',
    #                       'test',
    #                       'tester')
    # print_times(times)
    # results['add_user'] = times
    #
    # # time_add_status
    # print('\n'+'Timing add_status for Assignment #3 and #5:')
    # print('-----------------------------------------')
    # times = time_add_status('test123',
    #                       'test123_00001',
    #                       'Some silly status!')
    # print_times(times)
    # results['add_status'] = times
    #
    # # Print compiled results
    # print('Function              Assignment_03  Assignment_05')
    # print('--------------------------------------------------')
    # for key, value in results.items():
    #     print(key.ljust(20) + \
    #           '  '+'{0:.8f}'.format(value[0]).rjust(13) + \
    #           '  '+'{0:.8f}'.format(value[1]).rjust(13))
