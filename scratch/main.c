#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int make_ar(unsigned char* ar, int arsize){
    int i, tmp;
    srand(time(NULL));
    for (i=0; i<arsize; i++){
        int tmp = rand();
        ar[i] = (unsigned char) tmp % 255 + 1;
    }
    return 0;
}

int insert_sort(unsigned char* ar, int arsize){
    int i, j, key;
    
    for (j=1; j<arsize; j++){
        key = ar[j];
        i = j - 1;
        while (i >= 0 && ar[i] > key){
            ar[i+1] = ar[i];
            i--;
        }
        ar[i+1] = key;
    }
    return 0;
}

int merge(unsigned char* ar, int p, int q, int r){
    int n1 = q - p + 1;
    int n2 = r - q;
    unsigned char L[n1+1];
    unsigned char R[n2+1];
    int i, j;
    //printf("====\n");
    for (i=0; i<n1; i++){
        L[i] = ar[p+i];
        //printf("%d\n", (int) L[i]);
    }
    //printf("====\n");
    for(j=0; j<n2; j++){
        R[j] = ar[q+j+1];
        //printf("%d\n", (int) R[j]);
    }
    L[n1] = 255;
    R[n2] = 255;
    i = 0;
    j = 0;
    int k;
    for(k=p;k<=r;k++){
        if (L[i] <= R[j]){
            ar[k] = L[i];
            i++;
        }else{
            ar[k] = R[j];
            j++;
        }
    }
}

int merge_sort(unsigned char* ar, int p, int r){
    if (p < r){
        int q = (p+r)/2;
        merge_sort(ar, p, q);
        merge_sort(ar, q+1, r);
        merge(ar, p, q, r);
    }
    return 0;
}

int print_ar(unsigned char* ar, int arsize){
    int i;
    for (i=0; i<arsize; i++){
        printf("%d\n", (int) ar[i]);
    }
}

int save_ar(unsigned char* ar, int arsize, char* textname){
    FILE *f = fopen(textname, "w");
    if (f == NULL){
        printf("Error opening file!\n");
        exit(1);
    }
    int i;
    for (i=0; i<arsize; i++){
        fprintf(f, "%d\n", (int) ar[i]);
    }
    fclose(f);
}

int main (){
    int inputsize[8] = {100000, 500000, 750000, 1000000, 1500000, 2000000, 2500000, 3000000};
    int i, arsize;
    /*unsigned char ar[20];
    make_ar(ar, 20);
    print_ar(ar, 20);
    merge_sort(ar, 0, 20 - 1);
    char *fname = "idk.txt";
    save_ar(ar, 20, fname);
    */
    for (i=0; i<8; i++){
        arsize = inputsize[i];
        unsigned char ar[arsize];
        make_ar(ar, arsize);
        clock_t begin, end;
        double time_spent;

        begin = clock();
        //insert_sort(ar, arsize);
        merge_sort(ar, 0, arsize-1);
        end = clock();
        time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
        printf("time spent: %f \n", time_spent);
    }
    
}