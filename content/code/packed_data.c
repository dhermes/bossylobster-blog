// gcc -o main packed_data.c -std=c99 -pedantic
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Require that `double` is 64 bits / 8 bytes
#ifndef __STDC_IEC_559__
#error "IEEE 754 Required"
#endif

typedef struct Curve {
    uint32_t num_nodes;
    uint32_t dimension;
    double start;
    double end;
    double* nodes;
} Curve;

typedef double* PackedCurve;

const size_t NUM_NODES_OFFSET = 0;
const size_t DIMENSION_OFFSET = 1;
// START_OFFSET = ((DIMENSION_OFFSET + 1) * 4) / 8
const size_t START_OFFSET = 1;
// END_OFFSET = START_OFFSET + 1
const size_t END_OFFSET = 2;
// NODES_OFFSET = END_OFFSET + 1
const size_t NODES_OFFSET = 3;

size_t get_packed_size(uint32_t num_nodes, uint32_t dimension)
{
    /*
     * uint32_t num_nodes -> 4
     * uint32_t dimension -> 4
     * double   start     -> 8
     * double   end       -> 8
     * double*  nodes     -> 8 * size
     */
    return 24 + 8 * num_nodes * dimension;
}

PackedCurve make_curve(uint32_t num_nodes, uint32_t dimension)
{
    size_t packed_size = get_packed_size(num_nodes, dimension);

    PackedCurve curve_obj = (PackedCurve)malloc(packed_size);
    ((uint32_t*)curve_obj)[NUM_NODES_OFFSET] = num_nodes;
    ((uint32_t*)curve_obj)[DIMENSION_OFFSET] = dimension;
    ((double*)curve_obj)[START_OFFSET] = 0.0;
    ((double*)curve_obj)[END_OFFSET] = 1.0;

    return curve_obj;
}

void free_curve(PackedCurve curve_obj) { free(curve_obj); }

uint32_t get_num_nodes(PackedCurve curve_obj)
{
    return ((uint32_t*)curve_obj)[NUM_NODES_OFFSET];
}

uint32_t get_dimension(PackedCurve curve_obj)
{
    return ((uint32_t*)curve_obj)[DIMENSION_OFFSET];
}

double get_start(PackedCurve curve_obj)
{
    return ((double*)curve_obj)[START_OFFSET];
}

double get_end(PackedCurve curve_obj)
{
    return ((double*)curve_obj)[END_OFFSET];
}

double* get_nodes(PackedCurve curve_obj)
{
    return ((double*)curve_obj) + NODES_OFFSET;
}

size_t get_size(PackedCurve curve_obj)
{
    uint32_t num_nodes = get_num_nodes(curve_obj);
    uint32_t dimension = get_dimension(curve_obj);
    return get_packed_size(num_nodes, dimension);
}

void display_curve(PackedCurve curve_obj)
{
    uint32_t num_nodes = get_num_nodes(curve_obj);
    uint32_t dimension = get_dimension(curve_obj);

    printf("s in [%f, %f]\n", get_start(curve_obj), get_end(curve_obj));
    printf("%d x %d\n", num_nodes, dimension);

    double* nodes = get_nodes(curve_obj);
    printf("nodes:\n");
    for (size_t row = 0; row < num_nodes; row++) {
        printf("  |");
        size_t index = row;
        for (size_t col = 0; col < dimension; col++) {
            printf("%f|", nodes[index]);
            // Jump by an entire stride.
            index += num_nodes;
        }
        printf("\n");
    }

    printf("%ld bytes\n", get_packed_size(num_nodes, dimension));
}

int main(void)
{
    PackedCurve curve_obj = make_curve(3, 2);
    double* nodes = get_nodes(curve_obj);
    // Column 0
    nodes[0] = 0.0;
    nodes[1] = 1.0;
    nodes[2] = 3.0;
    // Column 1
    nodes[3] = 7.0;
    nodes[4] = 5.0;
    nodes[5] = 0.5;

    display_curve(curve_obj);

    free_curve(curve_obj);
    return 0;
}
