SHELL=/bin/sh
BENCHMARK=mg
BENCHMARKU=MG

include ../config/make.def

include ../sys/make.common

OBJS = mg.o \
		auto2_verify.o \
		${COMMON}/print_results.o  \
		${COMMON}/${RAND}.o \
		${COMMON}/c_timers.o \
		${COMMON}/wtime.o


${PROGRAM}: config ${OBJS}
	${CLINK} ${CLINKFLAGS} -o ${PROGRAM} ${OBJS} ${C_LIB}

.c.o:
	${CCOMPILE} $<

mg.o:		mg.c globals.h npbparams.h

clean:
	- rm -f *.o *~ 
	- rm -f npbparams.h core



