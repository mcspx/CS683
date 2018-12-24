#include <iostream>
#include <omp.h>

void matmul_depend(int M, int N, int P, int BS, int** A, int** B, int** C) // Assume BS divides N perfectly
{
    // Note 0: Assume BS divides N perfectly
    // Note 1: i, j, k, A, B, C are firstprivate by default
    // Note 2: A, B and C are just pointers
    
    int i, j, k, ii, jj, kk;
    
    for (i = 0; i < M; i+=BS) {
        for (j = 0; j < P; j+=BS) {
            for (k = 0; k < N; k+=BS) {
                #pragma omp task private(ii, jj, kk) \
                    depend (in: A[i:BS][k:BS], B[k:BS][j:BS]) \
                    depend (inout: C[i:BS][j:BS]) \
                    shared (C)
                for (ii = i; ii < i+BS; ii++ )
                    for (jj = j; jj < j+BS; jj++ )
                        for (kk = k; kk < k+BS; kk++ )
                            C[ii][jj] = C[ii][jj] + A[ii][kk] * B[kk][jj];
            }
        }
    }
}

int main(int argc, const char * argv[]) {
    const char * file_inp = "ab_large.in";
    const char * file_out = "c_large.out";
    
    int r_a, c_a, r_b, c_b;
    
    int** A, **B, **C;
    
    freopen(file_inp, "r", stdin);
    freopen(file_out, "w", stdout);
    
    std::cin  >> r_a >> c_a >> r_b >> c_b;
    std::cout << "Matrix multiply : A[" << r_a << "," << c_a << "] x B[" << r_b << "," << c_b << "]" << std::endl << std::endl;
    
    // ----------------------------------------
    
    A = (int**)malloc(sizeof(int*)*r_a);
    
    for(int r=0; r < r_a; r++) {
        A[r] = (int*)malloc(sizeof(int)*c_a);
        
        for(int c=0; c < c_a; c++) {
            std::cin >> A[r][c];
            //-- std::cout << A[r][c] << " ";
        }
        
        //-- std::cout << std::endl;
    }
    
    // ----------------------------------------
    
    B = (int**)malloc(sizeof(int*)*r_b);
    
    for(int r=0; r < r_b; r++) {
        B[r] = (int*)malloc(sizeof(int)*c_b);
        
        for(int c=0; c < c_b; c++) {
            std::cin >> B[r][c];
            //-- std::cout << B[r][c] << " ";
        }
        
        //-- std::cout << std::endl;
    }
    
    // ----------------------------------------
    
    C = (int**)malloc(sizeof(int*)*r_a);
    
    for(int r=0; r < r_a; r++) {
        C[r] = (int*)malloc(sizeof(int)*c_b);
        
        for(int c=0; c < c_b; c++) {
            C[r][c] = 0; // Initial all value to 0
        }
    }
    
    // ----------------------------------------
    
    int core = 4; // Number of CPU Core
    
    matmul_depend(r_a, c_a, c_b, core, A, B, C);
    
    for(int r=0; r < r_a; r++) {
        for(int c=0; c < c_b; c++) {
            std::cout << C[r][c] << " ";
        }
        
        std::cout << std::endl;
    }
    
    // ----------------------------------------
    
    fclose (stdout);
    fclose (stdin);
    
    return 0;
}
