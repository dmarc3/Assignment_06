# Assignment #6

Kathleen Wong wrote the profiling methods surrounding Assignment_03.
Marcus Bakke wrote the profiling methods surrounding Assignment_05.
All conclusions and observations were made together after discussing.

## 1. Summary of Profiling Results

Below represents the maximum time (as measured from `timeit.default_timer.timer`) based on executing each `main.py` method from Assignment_03 and Assignment_05 10 times sequentially. This is done via the `profile_methods.py` script. Note that this required some slight editting of Assignment_03 and Assignment_05 in order to import modules correctly. The base codes were unchanged.

| Method              | Assignment_03 | Assignment_05 |
| ------------------- | ------------: | ------------: |
| load_users          | 0.00000000    | 0.09767220    |
| load_status_updates | 0.00000000    | 5.52536620    |
| add_user            | 0.00000000    | 0.00295240    |
| add_status          | 0.00000000    | 0.00285300    |
| update_user         | 0.00000000    | 0.00339300    |
| update_status       | 0.00000000    | 0.00328830    |
| search_user         | 0.00000000    | 0.00374210    |
| search_status       | 0.00000000    | 0.02611800    |
| delete_user         | 0.00000000    | 0.00359320    |
| delete_status       | 0.00000000    | 0.02385740    |

## 2. Database Recommendation

Overall, we'd recommend the `MongoDB` implementation with the following caveats:
 - Having to handle the database relationships via code makes the code a bit more complicated as opposed to `SQL` and it's relational database properties. That said, the complexity increase is not significant.
 - Our current context manager setup needs to be looked at again. Specifically, we are regularly getting `pymongo` "connection closed" errors and have to be extremely careful with how we use `with MongoDBConnection()`.
 - We have some logic placed in the `menu.py` file for the `MongoDB` implementation which handles some of the relationship handling. This logic should be placed in `main.py` to stick with the overall goal of `menu.py` being replaced for a web-based user interface.

 The `MongoDB` implementation appears to be more performant. Additionally, `MongoDB`/`pymongo`'s `insert_many` method appears to have some memory handling that `peewee`/`SQL` does not. We noticed that we had to break the `insert_many` command for Assignment_03 into smaller chunks in order to run properly and the size of these chunks depends on the computer's specs. This is handled externally in Assignment_05 and makes that implementation more robust.