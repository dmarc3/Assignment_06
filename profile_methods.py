'''
Profiling Assignment_03 and Assignment_05.
Kathleen Wong focused on profiling Assignment_03 and peewee implementation.
Marcus Bakke focused on profiling Assignment_05 and MongoDB implementation.
'''
from timeit import default_timer as timer
import ipdb
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
        user_collection3 = main3.init_user_collection()
        if user_collection3.database.table_exists():
            user_collection3.database.drop_table()
            sn3.db.create_tables([sn3.Users])
    if del_status:
        status_collection3 = main3.init_status_collection()
        if status_collection3.database.table_exists():
            status_collection3.database.drop_table()
            sn3.db.create_tables([sn3.Status])
    
    # Assignment 05 Database
    if del_users:
        with sn5.MongoDBConnection() as mongo:
            user_collection5 = main5.init_user_collection(mongo)
            user_collection5.database.drop()
    if del_status:
        with sn5.MongoDBConnection() as mongo:
            status_collection5 = main5.init_status_collection(mongo)
            status_collection5.database.drop()

def time_load_users(filename: str):
    ''' Test load accounts method '''
    time3 = 0

    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Loading {filename} via Assignment_05... {i+1}')
            start = timer()
            result = main5.load_users(filename, main5.init_user_collection(mongo))
            end = timer()
            assert result == True
            if end - start > time5:
                time5 = end - start
            if i != NUM-1:
                reset_databases(1)

    return time3, time5

def time_load_status_updates(filename: str):
    ''' Test load status method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Loading {filename} via Assignment_05... {i+1}')
            start = timer()
            result = main5.load_status_updates(filename, main5.init_status_collection(mongo))
            end = timer()
            assert result == True
            if end - start > time5:
                time5 = end - start
            if i != NUM - 1:
                reset_databases(2)

    return time3, time5

def time_add_user():
    ''' Test load status method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Adding user via Assignment_05... {i+1}')
            start = timer()
            result = main5.add_user('test123',
                                    'test@gmail.com',
                                    'test',
                                    'tester',
                                    main5.init_user_collection(mongo))
            end = timer()
            assert result.acknowledged == True
            if end - start > time5:
                time5 = end - start
            result = main5.delete_user('test123',
                                       main5.init_user_collection(mongo))
            assert result == True

    return time3, time5

def time_add_status():
    ''' Test load status method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Adding status via Assignment_05... {i+1}')
            start = timer()
            result = main5.add_status('test123',
                                      'test123_00001',
                                      'Some silly status!',
                                      main5.init_status_collection(mongo))
            end = timer()
            assert result.acknowledged == True
            if end - start > time5:
                time5 = end - start
            result = main5.delete_status('test123_00001',
                                         main5.init_status_collection(mongo))
            assert result == True

    return time3, time5

def time_update_user():
    ''' Test load status method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Updating user via Assignment_05... {i+1}')
            start = timer()
            result = main5.update_user('Larisa.Yesima75',
                                       'test@gmail.com',
                                       'Larisa',
                                       'Yesima',
                                       main5.init_user_collection(mongo))
            end = timer()
            assert result.acknowledged == True
            if end - start > time5:
                time5 = end - start
            result = main5.update_user('Larisa.Yesima75',
                                       'Larisa.Yesima75@testmail.com',
                                       'Larisa',
                                       'Yesima',
                                       main5.init_user_collection(mongo))
            assert result.acknowledged == True

    return time3, time5

def time_update_status():
    ''' Test load status method '''
    time3 = 0
    # Update status 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Updating status via Assignment_05... {i+1}')
            start = timer()
            result = main5.update_status('Roshelle.Pironi69_275',
                                         'Roshelle.Pironi69',
                                         'test status text',
                                         main5.init_status_collection(mongo))
            end = timer()
            assert result == True
            if end - start > time5:
                time5 = end - start
            result = main5.update_status('Roshelle.Pironi69_275',
                                         'Roshelle.Pironi69',
                                         'didactic beginner counsel snotty cushion',
                                         main5.init_status_collection(mongo))
            assert result == True

    return time3, time5

def time_search_user():
    ''' Time search_user method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Searching user via Assignment_05... {i+1}')
            start = timer()
            result = main5.search_user('Roshelle.Pironi69',
                                       main5.init_user_collection(mongo))
            end = timer()
            assert bool(result) == True
            if end - start > time5:
                time5 = end - start

    return time3, time5

def time_search_status():
    ''' Time search_status method '''
    time3 = 0
    # Search users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Searching status via Assignment_05... {i+1}')
            start = timer()
            result = main5.search_status('Roshelle.Pironi69_275',
                                         main5.init_status_collection(mongo))
            end = timer()
            assert bool(result) == True
            if end - start > time5:
                time5 = end - start

    return time3, time5

def time_delete_user():
    ''' Time delete_user method '''
    time3 = 0
    # Load users 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Deleting user via Assignment_05... {i+1}')
            start = timer()
            result = main5.delete_user('Roshelle.Pironi69',
                                       main5.init_user_collection(mongo))
            end = timer()
            assert result == True
            if end - start > time5:
                time5 = end - start
            result = main5.add_user('Roshelle.Pironi69',
                                    'Roshelle.Pironi69@goodmail.com',
                                    'Roshelle',
                                    'Pironi',
                                    main5.init_user_collection(mongo))
            assert result.acknowledged == True

    return time3, time5

def time_delete_status():
    ''' Time delete_status method '''
    time3 = 0
    # Delete status 5 times via Assignment_05
    # Save max time
    time5 = 0
    for i in range(NUM):
        with sn5.MongoDBConnection() as mongo:
            print(f'  Deleting status via Assignment_05... {i+1}')
            start = timer()
            result = main5.delete_status('Zondra.Esme53_383',
                                         main5.init_status_collection(mongo))
            end = timer()
            assert result == True
            if end - start > time5:
                time5 = end - start
            result = main5.add_status('Zondra.Esme53',
                                      'Zondra.Esme53_383',
                                      'annoying advertisement bounce venomous battle',
                                      main5.init_status_collection(mongo))
            assert result.acknowledged == True

    return time3, time5

def print_times(times: list):
    ''' Print profile results '''
    print()
    print(f'          Assignment_03  Assignment_05')
    print(f'          -------------  -------------')
    print('Results:  '+'{0:.8f}'.format(times[0]).rjust(13) + \
          '  '+'{0:.8f}'.format(times[1]).rjust(13))
    print('\n')

if __name__ == '__main__':
    print(f'\nNUM set to: {NUM}')
    
    # Reset databases
    reset_databases(0)
    
    # Final results dictionary
    results = {'load_users': '',
               'load_status_updates': '',
               'add_user': '',
               'add_status': ''}

    # time_load_users
    print('\n'+'Timing load_users for Assignment #3 and #5:')
    print('-------------------------------------------')
    times = time_load_users('accounts.csv')
    print_times(times)
    results['load_users'] = times

    # time_load_status_updates
    print('\n'+'Timing load_status_updates for Assignment #3 and #5:')
    print('----------------------------------------------------')
    times = time_load_status_updates('status_updates.csv')
    print_times(times)
    results['load_status_updates'] = times

    # time_add_user
    print('\n'+'Timing add_user for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_add_user()
    print_times(times)
    results['add_user'] = times

    # time_add_status
    print('\n'+'Timing add_status for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_add_status()
    print_times(times)
    results['add_status'] = times

    # time_update_user
    print('\n'+'Timing update_user for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_update_user()
    print_times(times)
    results['update_user'] = times

    # time_update_status
    print('\n'+'Timing update_status for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_update_status()
    print_times(times)
    results['update_status'] = times

    # time_search_user
    print('\n'+'Timing search_user for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_search_user()
    print_times(times)
    results['search_user'] = times

    # time_search_status
    print('\n'+'Timing search_status for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_search_status()
    print_times(times)
    results['search_status'] = times  

    # time_delete_user
    print('\n'+'Timing delete_user for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_delete_user()
    print_times(times)
    results['delete_user'] = times  

    # time_delete_status
    print('\n'+'Timing delete_status for Assignment #3 and #5:')
    print('-----------------------------------------')
    times = time_delete_status()
    print_times(times)
    results['delete_status'] = times

    # Print compiled results
    print('Function              Assignment_03  Assignment_05')
    print('--------------------------------------------------')
    for key, value in results.items():
        print(key.ljust(20) + \
              '  '+'{0:.8f}'.format(value[0]).rjust(13) + \
              '  '+'{0:.8f}'.format(value[1]).rjust(13))
