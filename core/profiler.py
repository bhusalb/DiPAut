import cProfile

profile = cProfile.Profile()
import pstats


def run(func, args):
    profile.runcall(func, args)
    ps = pstats.Stats(profile)
    ps.sort_stats('cumtime')
    ps.print_stats(20)
