#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

void* thread_routine(void* arg) {
    int id = *(int*)arg;
    printf("thread %d: going to sleep\n", id);
    sleep(2);
    printf("thread %d: woke up\n", id);
    return NULL;
}

int main(void) {
    struct timespec start, end;
    
    clock_gettime(CLOCK_MONOTONIC, &start);

    pthread_t threads[4];
    int ids[4] = {1, 2, 3, 4};
    
    for (int i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, thread_routine, &ids[i]);
    
    for (int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);
        
    clock_gettime(CLOCK_MONOTONIC, &end);

    double elapsed = (end.tv_sec - start.tv_sec) + 
                     (end.tv_nsec - start.tv_nsec) / 1000000000.0;

    printf("all threads done\n");
    printf("Timp total real: %.2f secunde\n", elapsed);
    
    return 0;
}
