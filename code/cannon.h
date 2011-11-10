/* ===================================================================
 *
 * CS 566 - Assignment 03
 * Camillo Lugaresi, Cosmin Stroe
 *
 * Header file for shared declarations.
 *
 * =================================================================== */

#define VDIM 0
#define HDIM 1

struct problem {
	MPI_Comm mesh;
	int rank;
	int n;
	int k;
	int blksz;
	int blkcells;
	int p;
	int sqp;
	int coords[2];
	MPI_Comm hcomm, vcomm;
	struct matrix X;	// only root uses this
	int *Xblocks;
	struct matrix Xpow;	// only root uses this
	struct matrix Xb;	// original block:
	struct matrix A;	// cannon matrix 1
	struct matrix B;	// cannon matrix 2
	struct matrix C;	// cannon product
	int *temp;			// scratch space for shift
	MPI_Comm rowring;
	int rowblksz;
};

/* LU things */

#define MPI_number_type MPI_DOUBLE
#define number_type double

struct fmatrix {
	int n;
	number_type *data;
};
void alloc_fmatrix(struct fmatrix *m, int n);

struct pivot {
	int row;
	number_type value;
};

void best_pivot( void *invec, void *inoutvec, int *len, MPI_Datatype *datatype);
int setup_pivot_struct(MPI_Datatype *pivot_type, MPI_Op *best_pivot_op);
void LU_decomp(struct problem *info, struct fmatrix *X, int *reorder, MPI_Datatype pivot_type, MPI_Op best_pivot_op);
int count_swaps(int *reorder_all, int n);
number_type lu1d_determinant(struct problem *info);
number_type lu2d_determinant(struct problem *info);
