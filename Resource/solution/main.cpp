/* freopen example: redirecting stdout */
#include <stdio.h>
#include <iostream>
#include <omp.h>
using namespace std;
// Assume BS divides N perfectly
void matmul_depend(int M, int N, int P, int BS, int** A, int** B, int** C )
{
    int i, j, k, ii, jj, kk;
    for (i = 0; i < M; i+=BS) {
        for (j = 0; j < P; j+=BS) {
            for (k = 0; k < N; k+=BS) {
                // Note 1: i, j, k, A, B, C are firstprivate by default
                // Note 2: A, B and C are just pointers
                #pragma omp task private(ii, jj, kk) \
                    depend ( in: A[i:BS][k:BS], B[k:BS][j:BS] ) \
                    depend ( inout: C[i:BS][j:BS] ) \
                    shared (C)
                for (ii = i; ii < i+BS; ii++ )
                    for (jj = j; jj < j+BS; jj++ )
                        for (kk = k; kk < k+BS; kk++ )
                            C[ii][jj] = C[ii][jj] + A[ii][kk] * B[kk][jj];
            }
        }
    }
}
int main ()
{
    int r_a,c_a,r_b,c_b;
    freopen ("ab_large.in","r",stdin);
    freopen ("c_large.txt","w",stdout);
    //cout<<"This sentence is redirected to a file.\n";
    cin>> r_a >> c_a >> r_b >> c_b;
    cout<< r_a << endl <<c_a << endl << r_b << endl << c_b << endl;
    int** A, **B, **C;
    
    cout << "Debug1" <<endl;
    A = (int**)malloc(sizeof(int*)*r_a);
    for(int r=0; r<r_a; r++){
        A[r] = (int*)malloc(sizeof(int)*c_a);
        for(int c=0; c<c_a; c++){
            cin >> A[r][c];
            //cout << A[r][c] << " ";
        }
        //cout << endl;
    }

    B = (int**)malloc(sizeof(int*)*r_b);
    for(int r=0; r<r_b; r++){
        B[r] = (int*)malloc(sizeof(int)*c_b);
        for(int c=0; c<c_b; c++){
            cin >> B[r][c];
            //cout << B[r][c] << " ";
        }
        //cout << endl;
    }

    cout<<"Debug2"<<endl;
    C = (int**)malloc(sizeof(int*)*r_a);
    for(int r=0; r<r_a; r++){
        C[r] = (int*)malloc(sizeof(int)*c_b);
        for(int c=0; c<c_b; c++){
            C[r][c]=0;
        }
    }
    cout<<"Debug3"<<endl;

    cout<<"Debug4"<<endl;
    matmul_depend(r_a,c_a,c_b, 4, A, B, C);
    cout<<"Debug5"<<endl;
    for(int r=0; r<r_a; r++){
        for(int c=0; c<c_b; c++){
            cout << C[r][c] << " ";
        }
        cout << endl;
    }

    fclose (stdout);
    fclose (stdin);
    return 0;
}