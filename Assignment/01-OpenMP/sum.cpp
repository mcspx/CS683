#include <omp.h>
#include <stdio.h>

int main(void){
    int sum[8]={};
#pragma omp parallel shared(sum)
    {
        int ID = omp_get_thread_num();
        //int x[1000];
        
        int i; //initialization
        for(i=ID*1;i<(ID+1)*1;i++){
            sum[ID]+=i;
        }

        printf("L0-->core:%d, sum:%d \n",ID,sum[ID]);
#pragma omp barrier
        if(!(ID%2)){
            sum[ID]+=sum[ID+1];
            printf("L1-->core:%d, sum:%d\n",ID,sum[ID]);
        }
#pragma omp barrier
        if(!(ID%4)){
            sum[ID]+=sum[ID+2];
            printf("L2-->core:%d, sum:%d\n",ID,sum[ID]);
        }
#pragma omp barrier
        if(!(ID%8)){
            sum[ID]+=sum[ID+4];
            printf("L3-->core:%d, sum:%d\n",ID,sum[ID]);
        }
    }
    return 0;
}
