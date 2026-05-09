#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

int counter;

void* thread_routine(void* arg){
    int id = *(int*)arg;
    printf("Thread %d\n", id);
    for(int i = 0; i < 1e5; i++)
        counter++;
    return NULL;
}

int main(){
    pthread_t threads[2];
    int ids[2] = {1, 2};
    for(int i = 0; i < 2; i++)
        pthread_create(&threads[i], NULL, thread_routine, &ids[i]);
    for(int i = 0; i < 2; i++)
        pthread_join(threads[i], NULL);
    printf("Counter = %d\n", counter);
    return 0;
}
