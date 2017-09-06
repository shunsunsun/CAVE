from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
import os
import shutil

from spysmac.analyzer import Analyzer
from spysmac.html.html_builder import HTMLBuilder

from smac.utils.io.cmd_reader import CMDReader
from smac.scenario.scenario import Scenario
from smac.runhistory.runhistory import RunHistory


__author__ = "Joshua Marben"
__copyright__ = "Copyright 2017, ML4AAD"
__license__ = "3-clause BSD"
__maintainer__ = "Joshua Marben"
__email__ = "joshua.marben@neptun.uni-freiburg.de"

class SpySMACCLI(object):
    """
    SpySMAC command line interface.
    """

    def main_cli(self):
        """
        Main cli, implementing comparison between and analysis of SMAC-results.
        """
        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        req_opts = parser.add_argument_group("Required Options")
        req_opts.add_argument("--folders", required=True, nargs='+',
                              help="path(s) to SMAC output-directory/ies, "
                                   "containing each at least a runhistory and "
                                   "a trajectory.")

        opt_opts = parser.add_argument_group("Optional Options")
        opt_opts.add_argument("--verbose_level", default=logging.INFO,
                              choices=["INFO", "DEBUG"],
                              help="verbose level")
        opt_opts.add_argument("--output", default="",
                              help="Path to folder in which to save the combined HTML-report. "
                                   "If not specified, spySMAC will only generate "
                                   "the individual reports in the corresponding "
                                   "output-folders.")
        opt_opts.add_argument("--ta_exec_dir", default=None,
                              help="path to the execution-directory of the "
                                   "target algorithm. needed for validation.")
        args_, misc = parser.parse_known_args()

        if args_.verbose_level == "INFO":
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)

        logger = logging.getLogger('spysmac_cli')

        # SMAC results
        folders = args_.folders
        ta_exec_dir = args_.ta_exec_dir
        output = args_.output

        analyzer = Analyzer(folders, output, ta_exec_dir)
        analyzer.analyze()
