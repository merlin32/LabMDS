#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

typedef struct {
    int total_files;
    char** filenames;
    unsigned long* results;
    int* next_idx;
    pthread_mutex_t* lock;
} pool_arg_t;

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return 0;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);

    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);

    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }

    unsigned long sum = 0;
    for (int i = 0; i < 32; i++) sum += digest[i];
    return sum;
}

void* thread_routine(void* arg) {
    pool_arg_t* pool = (pool_arg_t*)arg;
    while (1) {
        int i;
        pthread_mutex_lock(pool->lock);
        if (*pool->next_idx >= pool->total_files) {
            pthread_mutex_unlock(pool->lock);
            break;
        }
        i = (*pool->next_idx)++;
        pthread_mutex_unlock(pool->lock);

        pool->results[i] = stretch_hash(pool->filenames[i]);
        printf("Thread processed %s (Result index %d)\n", pool->filenames[i], i);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <num_threads> <file1> <file2> ...\n", argv[0]);
        return 1;
    }

    int num_threads = atoi(argv[1]);
    int num_files = argc - 2;
    char** files = &argv[2];

    pthread_t threads[num_threads];
    unsigned long results[num_files];
    int next_idx = 0;
    pthread_mutex_t lock;
    pthread_mutex_init(&lock, NULL);

    pool_arg_t pool_arg = {num_files, files, results, &next_idx, &lock};

    int actual_threads = (num_threads < num_files) ? num_threads : num_files;

    for (int i = 0; i < actual_threads; i++)
        pthread_create(&threads[i], NULL, thread_routine, &pool_arg);

    for (int i = 0; i < actual_threads; i++)
        pthread_join(threads[i], NULL);

    pthread_mutex_destroy(&lock);

    printf("All tasks done\n");
    for (int i = 0; i < num_files + 1; i++)
        printf("Results[%d]: %lu\n", i, results[i]);

    return 0;
}
