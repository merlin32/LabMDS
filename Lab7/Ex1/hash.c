
#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000


const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
unsigned long results[4];

typedef struct {
    int id;
    const char* filename;
} thread_arg_t;

// you can ignore the details of this function beyond its signature 
unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
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
    thread_arg_t* data = (thread_arg_t*)arg;
    results[data->id] = stretch_hash(data->filename);
    printf("Thread %d finished processing %s\n", data->id, data->filename);
    return NULL;
}

int main(int argc, char** argv) {
    pthread_t threads[4];
    thread_arg_t args[4];
    for(int i = 0; i < 4; i++){
        args[i].id = i;
        args[i].filename = files[i];
        pthread_create(&threads[i], NULL, thread_routine, &args[i]);
    }
    
    for(int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);
    printf("All threads done\n");
    /*for(int i = 0; i < 4; i++)
        results[i] = stretch_hash(files[i]);*/
    for(int i = 0; i < 4; i++)
        printf("Results[%d]: %lu\n", i, results[i]); 
    return 0;
}
