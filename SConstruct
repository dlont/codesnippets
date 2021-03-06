import os, sys, subprocess
import hashlib

def PhonyTargets(env = None, **kw):
    if not env: env = DefaultEnvironment()
    for target,action in kw.items():
        env.AlwaysBuild(env.Alias(target, [], action))
        
env = Environment(ENV = os.environ)

output_dir = 'results/IntegralPlots'


ref_config = 'configs/conf_baseline_noOutliers_Multiclass_RF_cff.py'

dev_config = 'configs/conf_baseline_noOutliers_Multiclass_MLP_v1_cff.py'


configs_compare = ['configs/conf_cff.py','configs/conf_baseline_vanilla_cff.py']

configs = [dev_config]


# kbc_compare = env.Command([output_dir+'features_1d_Inflow_Outflow_p1.png',
#                   output_dir+'features_1d_Inflow_Outflow_p2.png',
#                   output_dir+'features_1d_Products_ActBalance_p1.png',
#                   output_dir+'features_1d_Products_ActBalance_p2.png',
#                   output_dir+'features_1d_Soc_Dem_p1.png',
#                   output_dir+'features_1d_Targets_p1.png',
#                   output_dir+'features_2d_Targets_correlations_p1.png'],
#              configs_compare,
#              "python3 bin/kbc_direct_marketing_mock.py -b -c $SOURCES --dir={0}".format(output_dir))

kbc = env.Command([output_dir+'Xfeatures_1d_Inflow_Outflow_p1.png',
                  output_dir+'Xfeatures_1d_Inflow_Outflow_p2.png',
                  output_dir+'Xfeatures_1d_Products_ActBalance_p1.png',
                  output_dir+'Xfeatures_1d_Products_ActBalance_p2.png',
                  output_dir+'Xfeatures_1d_Soc_Dem_p1.png',
                  output_dir+'Xfeatures_1d_Targets_p1.png',
                  output_dir+'Xfeatures_2d_Targets_correlations_p1.png'],
             [configs,"data/28_01_2020_1584entries/data_Products_ActBalance_default0.csv"],
             "python3 bin/kbc_direct_marketing_mock.py -c $SOURCES --dir={0}".format(output_dir))

PhonyTargets(env, make_output_folder = '-[ ! -d {0} ] && mkdir {0}'.format(output_dir))
PhonyTargets(env, trash_plots = '-rm {0}/features_* {0}/*learning_curve* {0}/*lasso_lars_ic_criterion* {0}/multiclass_classifier_distribution*'.format(output_dir))

kbc = env.Alias('kbc',['make_output_folder',kbc])
env.Alias('runall', ['trash_plots',kbc])
env.Alias('pred',[prediction])
# env.Alias('runcompareall', ['trash_plots',kbc_compare])

PhonyTargets(env, latex_report_clean = '-rm {0}/main.aux {0}/main.fdb_latexmk {0}/main.fls {0}/main.log {0}/main.pdf {0}/main.synctex.gz'.format('report'))

#custom print tree
git_tag = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip('\n')

def md5(fname):
    hash_md5 = hashlib.md5()
    result = ''
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        result = hash_md5.hexdigest()
    except Exception as e:
        print(e)
    return result

def get_all_children(node):
        return node.all_children()

def print_child_nodes(root, child_func, prune=0, showtags=0, margin=[0], visited=None):
    """
    Print a tree of nodes.  This is like render_tree, except it prints
    lines directly instead of creating a string representation in memory,
    so that huge trees can be printed.
    :Parameters:
        - `root`       - the root node of the tree
        - `child_func` - the function called to get the children of a node
        - `prune`      - don't visit the same node twice
        - `showtags`   - print status information to the left of each node line
        - `margin`     - the format of the left margin to use for children of root. 1 results in a pipe, and 0 results in no pipe.
        - `visited`    - a dictionary of visited nodes in the current branch if not prune, or in the whole tree if prune.
    """

    rname = str(root)


    # Initialize 'visited' dict, if required
    if visited is None:
        visited = {}

    if showtags:

        if showtags == 2:
            legend = (' E         = exists\n' +
                      '  R        = exists in repository only\n' +
                      '   b       = implicit builder\n' +
                      '   B       = explicit builder\n' +
                      '    S      = side effect\n' +
                      '     P     = precious\n' +
                      '      A    = always build\n' +
                      '       C   = current\n' +
                      '        N  = no clean\n' +
                      '         H = no cache\n' +
                      '\n')
            sys.stdout.write(legend)

        tags = [
            '[',
            ' E'[IDX(root.exists())],
            ' R'[IDX(root.rexists() and not root.exists())],
            ' BbB'[
                [0, 1][IDX(root.has_explicit_builder())] +
                [0, 2][IDX(root.has_builder())]
            ],
            ' S'[IDX(root.side_effect)], ' P'[IDX(root.precious)],
            ' A'[IDX(root.always_build)],
            ' C'[IDX(root.is_up_to_date())],
            ' N'[IDX(root.noclean)],
            ' H'[IDX(root.nocache)],
            ']'
        ]

    else:
        tags = []

    def MMM(m):
        return ["  ","| "][m]
    margins = list(map(MMM, margin[:-1]))

    children = child_func(root)

    if prune and rname in visited and children:
        sys.stdout.write(''.join(tags + margins + ['+-[', rname, ']']) + '\n')
        return

    # md5 = subprocess.check_output(["md5", "-q"])
    md5_checksum = md5(rname)
    sys.stdout.write(''.join(tags + margins + ['+-', rname, '\\nmd5:', md5_checksum, '\\ngit:', git_tag]) + '\n')

    visited[rname] = 1

    IDX = lambda N: N and 1 or 0

    if children:
        margin.append(1)
        idx = IDX(showtags)
        for C in children[:-1]:
            print_child_nodes(C, child_func, prune, idx, margin, visited)
        margin[-1] = 0
        print_child_nodes(children[-1], child_func, prune, idx, margin, visited)
        margin.pop()


AddOption('--mytree',
          dest='mytree',
          type='string',
          nargs='?',
          default='',
          action='store',
          metavar='DIR',
          help='print decorated build tree for graphviz')
my_tree = GetOption('mytree')

if my_tree != '':
    for item in BUILD_TARGETS:
        print_child_nodes(env.arg2nodes(item)[0],get_all_children)
    pass
