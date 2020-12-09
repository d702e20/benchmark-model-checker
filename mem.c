#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main () {
    char *temp;
    // malloc 1GB
    temp = malloc(1024000000);
    printf("Allocated mem\n");

    int t;
    sleep(2);
    for (int i = 0; i < 100000000; i++) {
        t += 5/2;
    }


    printf("Free mem\n");
    free(temp);

    return(0);
}
