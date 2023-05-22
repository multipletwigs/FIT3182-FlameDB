from runner import *
import matplotlib.pyplot as plt
import numpy as np
import argparse

def generate_graph(results, test_combinations, key, y_axis):
  sizes = results[-1]['MAX_SIZES']
  GLS_insert_amp = [result[key] for result in results if result['exp'] == 'GLS' and result['bf'] == 'HEBF']
  Trad_insert_amp = [result[key] for result in results if result['exp'] == 'Traditional LSM' and result['bf'] == 'HEBF']

  X_sizes = np.arange(len(sizes))
    
  plt.bar(X_sizes - 0.2, GLS_insert_amp, 0.4, label = 'GLS')
  plt.bar(X_sizes + 0.2, Trad_insert_amp, 0.4, label = 'LSM')
    
  plt.xticks(X_sizes, sizes)
  plt.xlabel("Level Sizes")
  plt.ylabel(y_axis)
  plt.title(f"{y_axis} across different sizes")
  plt.legend()
  plt.savefig(f'results/{y_axis}.png')
  plt.clf()

def run_benchmark(gls, hobf, all):
    MAX_SIZES = [10, 50, 100]
    SIZE_MULTIPLE = 5 # Usually the next level is around 5 times bigger than the original one

    if not os.path.exists("results"):
      os.makedirs("results")
  
    if all:
        test_combinations = [(gls, hobf) for gls in [True, False] for hobf in [True, False]]
    else:
        test_combinations = [(gls, hobf)]

    results = []
    for MAX_SIZE in MAX_SIZES:
        for gls, hobf in test_combinations:
            print(f"---- Running benchmark for {'GLS' if gls else 'Traditional LSM'} with {'HOBF' if hobf else 'HEBF'} where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
            # Before running the test, purge the harddisk first to reset disk amplification
            clear_harddisk()
            insert_amp, search_amp, total_insert_size, total_buffer_used, total_search_size, total_search_buffer_used = LSM_Insert(gls=gls, benchmark=True, max_size=MAX_SIZE, size_multiple=SIZE_MULTIPLE, hobf=hobf)
            results.append({
              'exp': 'GLS' if gls else 'Traditional LSM',
              'bf': 'HOBF' if hobf else 'HEBF',
              'insert_amp': insert_amp,
              'search_amp': search_amp,
              'MAX_SIZES': MAX_SIZES,
              'total_insert_size':total_insert_size, 
              'total_buffer_used': total_buffer_used,
              'total_search_size': total_search_size,
              'total_search_buffer_used': total_search_buffer_used
            })

    # Generate graphs based on the results into results directory 
    generate_graph(results, test_combinations, key="insert_amp", y_axis="Write amplification")
    generate_graph(results, test_combinations, key="search_amp", y_axis="Read amplification")
    generate_graph(results, test_combinations, key="total_buffer_used", y_axis="Total bytes used for writing")

def purge_command(args):
    clear_harddisk()

def gls_command(args):
    if args.hobf:
        print(f"---- Running GLS with HOBF where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=True, benchmark=False, max_size=MAX_SIZE, size_multiple=SIZE_MULTIPLE, hobf=True)
    elif args.hebf:
        print(f"---- Running GLS with HEBF where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=True, benchmark=False, max_size=MAX_SIZE, size_multiple=SIZE_MULTIPLE, hobf=False)
    else:
        print("Please specify either --hobf or --hebf with --gls.")

def trad_command(args):
    if args.hobf:
        print(f"---- Running Traditional LSM with HOBF where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=False, benchmark=False, max_size=MAX_SIZE, size_multiple=SIZE_MULTIPLE, hobf=True)
    elif args.hebf:
        print(f"---- Running Traditional LSM with HEBF where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=False, benchmark=False, max_size=MAX_SIZE, size_multiple=SIZE_MULTIPLE, hobf=False)
    else:
        print("Please specify either --hobf or --hebf with --trad.")

def benchmark_command(args):
    run_benchmark(args.gls, args.hobf, args.all)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="LSM")
    subparsers = parser.add_subparsers()

    # Subparser for the purge command
    purge_parser = subparsers.add_parser('purge', help='Clear harddisk after execution')
    purge_parser.set_defaults(func=purge_command)

    # Subparser for the gls command
    gls_parser = subparsers.add_parser('gls', help='Use GLS compaction algorithm')
    gls_parser.add_argument('--hobf', action='store_true', help='Use homogenous bloom filters')
    gls_parser.add_argument('--hebf', action='store_true', help='Use heterogenous bloom filters')
    gls_parser.set_defaults(func=gls_command)

    # Subparser for the trad command
    trad_parser = subparsers.add_parser('trad', help='Use traditional compaction algorithm (Levels DB)')
    trad_parser.add_argument('--hobf', action='store_true', help='Use homogenous bloom filters')
    trad_parser.add_argument('--hebf', action='store_true', help='Use heterogenous bloom filters')
    trad_parser.set_defaults(func=trad_command)

    # Subparser for the benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run benchmark')
    benchmark_parser.add_argument('--gls', action='store_true', help='Use GLS compaction algorithm')
    benchmark_parser.add_argument('--hobf', action='store_true', help='Use homogenous bloom filters')
    benchmark_parser.add_argument('--all', action='store_true', help="Run all tests")
    benchmark_parser.set_defaults(func=benchmark_command)

    args = parser.parse_args()

    MAX_SIZE = 50
    SIZE_MULTIPLE = 5

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()