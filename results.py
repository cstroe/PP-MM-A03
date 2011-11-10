#!/usr/bin/env python
import re
import os
from collections import defaultdict
import sys

out_dir = "out"

#cannon_1_1_1_1024_16_0.3_0.3.output
name_re = re.compile("([^.]+)_(\\d+)_(\\d+)_(\\d+)_(-[^_]*_)*(\\d+)_(\\d+)_(.*)\.output")
time_re = re.compile("(.*) time: (\\d+\.\\d+)")

times = defaultdict(lambda: defaultdict(list))
progset = set()
proccoresets = defaultdict(set)
nset = set()
kset = set()
progs = defaultdict(lambda: {
	'proccoresets':defaultdict(set),
	'nset':set(),
	'kset':set()
	})

for file_name in os.listdir(out_dir):
	m = name_re.match(file_name)
	if not m: continue
	prog = m.group(1)
	run, procs, cores = (int(x) for x in m.group(2,3,4))
	opts = m.group(5)
	if opts:
		prog += ' ' + ' '.join(opts.strip('_').split('_'))
	n, k = (int(x) for x in m.group(6,7))
	got_time = False
	with open(os.path.join(out_dir,file_name)) as f:
		for line in f:
			m = time_re.match(line)
			if not m: continue
			got_time = True
			stage = m.group(1)
			time = float(m.group(2))
			times[stage][(prog, procs, cores, n, k)].append(time)
	if not got_time:
		sys.stderr.write("bad file? %s\n" % (file_name,))
		continue
	progset.add(prog)
	proccoresets[procs].add(cores)
	progs[prog]['proccoresets'][procs].add(cores)
	nset.add(n)
	kset.add(k)
	progs[prog]['nset'].add(n)
	progs[prog]['kset'].add(k)

SEP="&"

stage_captions = {
	'total': 'Total runtime',
	'matrix multiplication': 'Multiplication time',
	'LU': 'LU decomposition time',
}

program_captions = {
	'cannon': 'Cannon',
	'cannon -s': 'Cannon/Strassen',
	'dns': 'DNS',
	'dns -s': 'DNS/Strassen',
}

#proclist = sorted(proccoresets.keys())
#nlist = sorted(nset)
#klist = sorted(kset)
for stage in [ 'total', 'matrix multiplication', 'LU']:
	for prog in ["cannon", "cannon -s", "dns", "dns -s"]:#sorted(progset):
		proclist = sorted(progs[prog]['proccoresets'].keys())
		nlist = sorted(progs[prog]['nset'])
		klist = sorted(progs[prog]['kset'])

		
		print """\\begin{table}[h]
	\\centering"""
		
		print """\\begin{tabular}{|"""+("" if stage == 'LU' else 'r')+"""r|"""+"r|"*sum(len(progs[prog]['proccoresets'][procs]) for procs in proclist)+"""}"""
		print "\\hline"
#		print """\multicolumn{2}{c}{\multirow{2}{*}{\backslashbox{n}{$(p,k)$}}}""", 
# 		print "", SEP, """p""", 
# 		for procs in proclist:
# 			print SEP, """\multicolumn{%d}{c}{$%d$}""" % (len(progs[prog]['proccoresets'][procs]), procs),
# 		print "\\\\"
		if stage == 'LU':
			print """\\backslashbox{n}{p,c}""",
		else:
			print "", SEP, """\\backslashbox{k}{p,c}""",
		for procs in proclist:
			for cores in sorted(progs[prog]['proccoresets'][procs]):
				print SEP, "(%d,%d)" %(procs,cores),
		print "\\\\"
		print "\\hline"
		if stage != 'LU':
			print """\\makebox(0,0){\\put(0,2.375\\normalbaselineskip){\\rlap{n}}}"""
		
		for n in nlist:
			first = True
			if stage == 'LU':
				print n,
				for procs in proclist:
					for cores in sorted(progs[prog]['proccoresets'][procs]):
						timelist = []
						for k in klist:
							timelist += times[stage][(prog, procs, cores, n, k)]
						if len(timelist) == 0: print SEP, "-",
						else: print SEP, "%.3f" % (sum(timelist) / float(len(timelist))),
				print "\\\\"
			else:
				for k in klist:
					if first:
						print """\\multirow{2}{*}{%d}""" %(n,),
						first = False
					print SEP, k
					for procs in proclist:
						for cores in sorted(progs[prog]['proccoresets'][procs]):
							timelist = times[stage][(prog, procs, cores, n, k)]
							if len(timelist) == 0: print SEP, "-",
							else: print SEP, "%.3f" % (sum(timelist) / float(len(timelist))),
					print "\\\\"
			print "\\hline"
		print """\\end{tabular}"""
		
		print """\\caption{%s (in seconds) for the %s formulation.}
	\\label{tab:%s}
\\end{table}""" % (stage_captions[stage], program_captions.get(prog, prog), prog+stage)
	print


# compare LU 1 and 2
for stage in [ 'total', 'LU']:
	for prog in ["cannon -2"]:#sorted(progset):
		proclist = sorted(progs[prog]['proccoresets'].keys())
		nlist = sorted(progs[prog]['nset'])
		klist = sorted(progs[prog]['kset'])

		
		print """\\begin{table}[h]
	\\centering"""
		
		print """\\begin{tabular}{|rr|"""+"r|"*sum(len(progs[prog]['proccoresets'][procs])*2 for procs in proclist)+"""}"""
		print "\\hline"
#		print """\multicolumn{2}{c}{\multirow{2}{*}{\backslashbox{n}{$(p,k)$}}}""", 
# 		print "", SEP, """p""", 
# 		for procs in proclist:
# 			print SEP, """\multicolumn{%d}{c}{$%d$}""" % (len(progs[prog]['proccoresets'][procs]), procs),
# 		print "\\\\"
		print "", SEP, """\\multirow{2}{*}{\\backslashbox{k}{p,c}}""",
		for procs in proclist:
			for cores in sorted(progs[prog]['proccoresets'][procs]):
				print SEP, """\multicolumn{2}{c|}{(%d,%d)}""" %(procs,cores),
		print "\\\\"
		print "n", SEP, "",
		for procs in proclist:
			for cores in sorted(progs[prog]['proccoresets'][procs]):
				print SEP, "1d", SEP, "2d",		
		print "\\\\"
		print "\\hline"
		
		for n in nlist:
			first = True
			for k in klist:
				if first:
					print n,
					first = False
				print SEP, k
				for procs in proclist:
					for cores in sorted(progs[prog]['proccoresets'][procs]):
						for prog2 in ["cannon", "cannon -2"]:
							timelist = times[stage][(prog2, procs, cores, n, k)]
							if len(timelist) == 0: print SEP, "-",
							else: print SEP, "%.3f" % (sum(timelist) / float(len(timelist))),
				print "\\\\"
			print "\\hline"
		print """\\end{tabular}"""
		
		print """\\caption{%s (in seconds) for the Cannon formulation with 1D and 2D LU decomposition.}
	\\label{tab:lucompare_%s}
\\end{table}""" % (stage_captions[stage], stage)
	print



# program comparison graphs
proclist = sorted(proccoresets.keys())
progl = ['cannon', 'cannon -s', 'dns', 'dns -s']
SEP=":"
for n in nset:
	for k in kset:
		with open("graphs/cannon-dns-%d-%d.txt" % (n,k), "w") as f:
			f.write( "(%d,%d) " % (n, k) )
			f.write( ','.join(progl) + "\n\n" )
			for procs in proclist:
				for cores in proccoresets[procs]:
					f.write( "(%d,%d)" % (procs, cores) )
					for prog in progl:
						timelist = times['total'][(prog, procs, cores, n, k)]
						if len(timelist) == 0: f.write( SEP + "-" )
						else: f.write( SEP + "%.3f" % (sum(timelist) / float(len(timelist))) )
					f.write("\n")
			f.write("\n")
			f.write("\n")

with open("graphs/cannon-dns.plt", "w") as f:
	f.write("""#!/usr/bin/gnuplot -persist

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

set terminal postscript enhanced color\n""")
	for n in nset:
		for k in kset:
			name = "cannon-dns-%d-%d" % (n,k)
			f.write("""set output '| ps2pdf - ../images/%s.pdf'

plot '%s.txt' using 2:xticlabels(1) with lines lw 3 title "cannon", \\
     '%s.txt' using 3:xticlabels(1) with lines lw 3 title "cannon strassen", \\
     '%s.txt' using 4:xticlabels(1) with lines lw 3 title "dns", \\
     '%s.txt' using 5:xticlabels(1) with lines lw 3 title "dns strassen"\n
""" % (name, name, name, name, name))

# SEP=":"
# for prog in sorted(progset):
# 	print prog,
# 	for n in nlist:
# 		for k in klist:
# 			print SEP, "(%d,%d)" % (n, k),
# 	print
# 	for procs, cores in proccorelist:
# 		print "(%d,%d)" % (procs, cores),
# 		
# 		for n in nlist:
# 			for k in klist:
# 				for stage in ['matrix multiplication', 'LU', 'total']:
# 					timelist = times[stage][(prog, procs, cores, n, k)]
# 					if len(timelist) == 0: print SEP, "-",
# 					else: print SEP, "%.3f" % (sum(timelist) / float(len(timelist))),
# 		print
# 
# print progset