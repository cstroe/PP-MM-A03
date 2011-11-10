#!/usr/bin/gnuplot -persist

#set title "101-303 with e=0.2, clTh=0.1"
set notitle
set auto x
set auto y
#set xtics 10 
#set ytics 5
#set style data lines
#set style fill solid border -1
#set style histogram cluster gap 5
set boxwidth 0.9

#set log y

set ylabel "Runtime (s)"
set xlabel "(processors, cores)"


set grid noxtics nomxtics ytics mytics 
#unset key
set key right top


#set lmargin 4
#set rmargin 3.5

set datafile separator ":"

set bmargin 0
#set lmargin 3
set tmargin 0
set rmargin 1

set terminal postscript enhanced color
set output '| ps2pdf - ../images/cannon-dns-1024-4.pdf'

plot 'cannon-dns-1024-4.txt' using 2:xticlabels(1) with lines lw 3 title "cannon", \
     'cannon-dns-1024-4.txt' using 3:xticlabels(1) with lines lw 3 title "cannon strassen", \
     'cannon-dns-1024-4.txt' using 4:xticlabels(1) with lines lw 3 title "dns", \
     'cannon-dns-1024-4.txt' using 5:xticlabels(1) with lines lw 3 title "dns strassen"
