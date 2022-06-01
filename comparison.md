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

1. Based on your results and on **your experience implementing both databases**, make a recommendation as to which one should be implemented. Performance is key, but include other technical aspects such as ease of implementation if appropriate.