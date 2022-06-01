# Assignment #6

Kathleen Wong wrote the profiling methods surrounding Assignment_03.
Marcus Bakke wrote the profiling methods surrounding Assignment_05.
All conclusions and observations were made together after discussing.

## 1. Summary of Profiling Results

Below represents the maximum time (as measured from `timeit.default_timer.timer`) based on executing each `main.py` method from Assignment_03 and Assignment_05 10 times sequentially. This is done via the `profile_methods.py` script. Note that this required some slight editting of Assignment_03 and Assignment_05 in order to import modules correctly. The base codes were unchanged.

| Method              | Assignment_03 | Assignment_05 |
| ------------------- | ------------: | ------------: |
| load_users          |    0.09297980 |    0.13432020 |
| load_status_updates |    7.87610780 |    6.03636770 |
| add_user            |    0.01244940 |    0.00382000 |
| add_status          |    0.02728510 |    0.01917810 |
| update_user         |    0.01293120 |    0.00451330 |
| update_status       |    0.02698020 |    0.00432690 |
| search_user         |    0.00065890 |    0.00450450 |
| search_status       |    0.00057320 |    0.00349650 |
| delete_user         |    0.02364490 |    0.02807180 |
| delete_status       |    0.01253790 |    0.02256320 |

## 2. Database Recommendation

Overall, we'd recommend the `MongoDB` implementation with the following caveats:
 - Having to handle the database relationships via code makes the code a bit more complicated as opposed to `SQL` and it's relational database properties. That said, the complexity increase is not significant.
 - Our current context manager setup needs to be looked at again. Specifically, we are regularly getting `pymongo` "connection closed" errors and have to be extremely careful with how we use `with MongoDBConnection()`.
 - We have some logic placed in the `menu.py` file for the `MongoDB` implementation which handles some of the relationship handling. This logic should be placed in `main.py` to stick with the overall goal of `menu.py` being replaced for a web-based user interface.

 The `MongoDB` implementation appears to be more performant. Additionally, `MongoDB`/`pymongo`'s `insert_many` method appears to have some memory handling that `peewee`/`SQL` does not. We noticed that we had to break the `insert_many` command for Assignment_03 into smaller chunks in order to run properly and the size of these chunks depends on the computer's specs. This is handled externally in Assignment_05 and makes that implementation more robust.