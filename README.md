# Matrix Multiplication using the Message Passing Interface (MPI) API

This repository started out as a class project for the [Parallel Processing course](https://www.cs.uic.edu/~ajayk/c566/c566fa12.html) at [UIC](https://www.cs.uic.edu/) with [Professor Kshemkalyani](https://www.cs.uic.edu/~ajayk/).

Several matrix multiplication algorithms are implemented in C, timings are recorded and a report was written.

## Generating the report

On Ubuntu, the `texlive-full` package is required:

    sudo apt install texlive-full

Then, to generate the PDF report type:

    make

This will produce [document.pdf](document.pdf).

## Related Links
* [go-mpi](https://github.com/JohannWeging/go-mpi) - [golang](https://golang.org/) bindings for [MPI](http://mpi-forum.org/)
