#import sys
import pyshield as ps
import shutil
import os
import argparse


#SHORTARGS = ['--c'=, '--get']

#def usage():
#    print(('pyshield --execute --> runs calculations. \n'
#           'pyshield --execute --config myconfig.yml --> runs calculations using specified config file. \n'
#           'pyshield --get_config myconfig.yml --> creates a config file with all options set to default values.\n'
#           'pyshield --get_example --> creates an example config, source definitions, barrier definitions and point definitions.\n'))
#    
def main(args=None):
    """The main routine."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    

    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('--execute', help='Do calculations', 
                        action='store_true')
    
    
    
    group.add_argument('--getconfig', default=ps.CONFIG_FILE,
                        help=('Creates a config file with all options '
                              'set to default values.'))
    group.add_argument('--getexample', action='store_true',
                        help='Create example files in current folder')
    
    group2 = parser.add_mutually_exclusive_group()
    
    group2.add_argument('--grid', action='store_true',
                        help='Calculate dose maps on grid')
                      
    group2.add_argument('--points', action='store_true',
                       help='Calculate dose in defined points')
    
    parser.add_argument('--config', default=ps.CONFIG_FILE,
                        help='Specify config file. config.yml will be loaded '
                        'by default if present.')
                      
    parser.add_argument('--log', default=ps.LOG_ERROR,
                        choices=[ps.LOG_DEBUG, ps.LOG_INFO, ps.LOG_ERROR],
                        help='Specify log level')
                       
    
    example = ('Example of use:\n\n'
               'pyshield --execute --points\n\n'
               'Runs calculations for specified dose points.:\n'
               '\tbarriers.yml: barrier defintions\n'
               '\tsources.yml: source definitions\n'
               '\tpoints.yml: points in which the dose is calculated\n\n'
               'pyshield --execute --grid --config myconfig.yml\n\n'
               'Calculate dosemaps and override settings from myconfig.yml.'
               '\tbarriers.yml: barrier defintions\n'
               '\tsources.yml: source definitions\n\n'
               'pyshield --getconfig myconfig.yml\n\n'
               'Creates myconfig.yml in current folder with all settings '
               'set to default.\n\n'
               'pyshield --getexample\n\n'
               'Create example files in current folder.')
    
    parser.epilog = example
    args = parser.parse_args()
    
    
    ps.COMMAND_LINE = True # run from command line
    
    if args.execute:
        if args.grid and args.points:
            calculate = [ps.GRID, ps.POINTS]
        elif args.grid:
            calculate = ps.GRID
        elif args.points:
            calculate = ps.POINTS
        else:
            msg = '--grid or --points or both should be specified.'
            raise argparse.ArgumentError(msg)
        ps.run(config=args.config, calculate=calculate)
        
    elif args.getconfig:
        file = args.getconfig
        if overwrite(file):
            shutil.copyfile(os.path.join(ps.__pkg_root__, ps.DEF_CONFIG_FILE),
                            ps.CONFIG_FILE)
    elif args.getexample:
        files = ['barriers.yml', 'config.yml', 'points.yml', 'sources.yml']
        for file in files:
            fullfile = os.path.join(ps.__pkg_root__, 'example', file)
            if overwrite(file):
                shutil.copyfile(fullfile, file)
                            
    else:
        parser.print_help()

def overwrite(file):
    if not os.path.exists(file):
        write=True
    else:        
        answer = False
        while not answer:    
            ask=input('\nOverwrite {0} Y/n: '.format(file))
            if ask.lower().strip()=='n':
                answer=True
                write = False
            elif ask.strip() == 'Y':
                answer=True
                write=True       
    return write
if __name__ == "__main__":
    main()