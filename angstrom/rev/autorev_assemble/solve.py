# solve.py
import angr

#p = angr.Project('./a.out', load_options={'auto_load_libs': False})

addr_main = 0x407971
addr_succeeded = 0x40894c
addr_failed = 0x40895a
#addr_main = p.loader.main_bin.get_symbol('main').addr
#addr_succeeded = p.loader.main_bin.get_symbol('succeeded').addr
#addr_failed = p.loader.main_bin.get_symbol('failed').addr
#print("main = %x" % addr_main)
#print("succeeded = %x" % addr_succeeded)
#print("failed = %x" % addr_failed)
#
#initial_state = p.factory.blank_state(addr=addr_main)
#initial_path = p.factory.path(initial_state)
#pg = p.factory.path_group(initial_path)
#e = pg.explore(find=(addr_succeeded,), avoid=(addr_failed,))
#
#if len(e.found) > 0:
#    print('Dump stdin at succeeded():')
#    s = e.found[0].state
#    print("%r" % s.posix.dumps(0))

import sys

def basic_symbolic_execution():
	p = angr.Project('./autorev_assemble')

# Now, we want to construct a representation of symbolic program state.
# SimState objects are what angr manipulates when it symbolically executes
# binary code.
# The entry_state constructor generates a SimState that is a very generic
# representation of the possible program states at the program's entry
# point. There are more constructors, like blank_state, which constructs a
# "blank slate" state that specifies as little concrete data as possible,
# or full_init_state, which performs a slow and pedantic initialization of
# program state as it would execute through the dynamic loader.

	state = p.factory.entry_state()

# Now, in order to manage the symbolic execution process from a very high
# level, we have a SimulationManager. SimulationManager is just collections
# of states with various tags attached with a number of convenient
# interfaces for managing them.

	sm = p.factory.simulation_manager(state)
	sm.explore(find=addr_succeeded, avoid=[addr_failed])
# Now, we begin execution. This will symbolically execute the program until
# we reach a branch statement for which both branches are satisfiable.

	sm.run(until=lambda sm_: len(sm_.active) > 1)
	s = sm.found[0]
	print(sm.found[0].posix.dumps(0))
	#input_0 = sm.active[0].posix.dumps(0)
	#input_1 = sm.active[1].posix.dumps(0)
	print(s)
# We have used a utility function on the state's posix plugin to perform a
# quick and dirty concretization of the content in file descriptor zero,
# stdin. One of these strings should contain the substring "SOSNEAKY"!


if __name__ == '__main__':
	basic_symbolic_execution()
#	sys.stdout.buffer.write(basic_symbolic_execution())

