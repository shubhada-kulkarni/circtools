#!/usr/bin/env python3

# Copyright (C) 2017 Tobias Jakobi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
import os.path

# global settings
version = "0.0.1a"
program_name = "circtools"

# samtools/git like parsing from http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html


def main():
    CircTools()


class CircTools(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Looks like samtools",
            usage="""circtools [-V] <command> [<args>]
            Available commands:

               enrich       circular RNA RBP enrichment scan
               primer       circular RNA primer design tool
               detect       circular RNA detection with DCC
               reconstruct  circular RNA reconstruction with FUCHS

            """)
        parser.add_argument("command", help="Command to run")

        parser.add_argument("-V",
                            "--version",
                            action="version",
                            version=version
                            )

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("The supplied command is unknown")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def enrich():

        # build the argument list
        parser = argparse.ArgumentParser(
            description="circular RNA RBP enrichment tools")

        # REQUIRED ARGUMENTS
        group = parser.add_argument_group("Required options")

        group.add_argument("-c",
                           "--circ-file",
                           dest="circ_rna_input",
                           help="Path to the CircRNACount file generated by DCC",
                           required=True
                           )

        group.add_argument("-b",
                           "--bed-input",
                           dest="bed_input",
                           help="One or more BED files containing features to overlap",
                           required=True
                           )

        group.add_argument("-a",
                           "--annotation",
                           dest="annotation",
                           help="Genome reference annotation file used to not shuffle into intragenic regions",
                           required=True
                           )

        group.add_argument("-g",
                           "--genome",
                           dest="genome_file",
                           help="Genome file for use with bedtools shuffle. See bedtools man page for details.",
                           required=True
                           )

        # OPTIONAL ARGUMENTS
        group = parser.add_argument_group("Additional options")

        group.add_argument("-o",
                           "--output",
                           dest="output_directory",
                           default="./",
                           help="The output folder for files created by " + program_name + " [default: .]",
                           )

        group.add_argument("-i",
                           "--iterations",
                           dest="num_iterations",
                           help="Number of iterations for CLIP shuffling [default: 1000]",
                           type=int,
                           default=1000
                           )

        group.add_argument("-p",
                           "--processes",
                           dest="num_processes",
                           help="Number of threads to distribute the work to",
                           type=int,
                           default=1
                           )

        group.add_argument("-t",
                           "--temp",
                           dest="tmp_directory",
                           help="Temporary directory used by pybedtools",
                           default="/tmp/"
                           )

        group.add_argument("-T",
                           "--threshold",
                           dest="threshold",
                           help="p-value cutoff",
                           type=int,
                           default=2
                           )

        group.add_argument("-P",
                           "--pval",
                           dest="pval",
                           help="p-value cutoff",
                           type=float,
                           default=0.05
                           )

        group.add_argument("-H",
                           "--header",
                           dest="has_header",
                           help="Defines if the circRNA input file has a header line [default: no]",
                           type=bool,
                           default=False
                           )

        group.add_argument("-F",
                           "--output-filename",
                           dest="output_filename",
                           help="Defines the output file prefix [default: output]",
                           default="output"
                           )
        args = parser.parse_args(sys.argv[2:])

        # make sure we can load the sub module
        sys.path.append(os.path.join(os.path.dirname(__file__)))

        # start the enrichment module
        import enrichment.enrichment_check
        enrich = enrichment.enrichment_check.EnrichmentModule(args, program_name, version)
        enrich.run_module()

    @staticmethod
    def primer():
        parser = argparse.ArgumentParser(
            description="circular RNA primer design")
        # NOT prefixing the argument with -- means it"s not optional

        group = parser.add_argument_group("Input")
        group.add_argument("-c",
                           "--circFile",
                           dest="circFile",
                           help="A tab/comma separated file of splice junction coordinates with the columns ordered as:\
                            chromosome, start, end, strand",
                           )
        group.add_argument("-e",
                           "--ensPackage",
                           dest="ensPackage",
                           help="An ensembldb package name, e.g. EnsDb.Hsapiens.v86",
                           )
        group.add_argument("-b",
                           "--bsgPackage",
                           dest="bsgPackage",
                           help="BSGenome package name, e.g. BSgenome.Hsapiens.NCBI.GRCh38",
                           )

        group = parser.add_argument_group("Processing")
        group.add_argument("-t",
                           "--typeExons",
                           dest="typeExons",
                           help="Longest|shortest|all exons to use for primer design",
                           )

        group = parser.add_argument_group("Output")
        group.add_argument("-r",
                           "--reportFile",
                           dest="reportFile",
                           help="A filename for an  HTML report with exon sequences [Default: report.html]",
                           )
        group.add_argument("-p",
                           "--primerFile",
                           dest="primerFile",
                           help="A filename for an... [Default: primers.tsv]",  # Todo: help text missing
                           )
        group.add_argument("-u",
                           "--productFile",
                           dest="productFile",
                           help="A filename for an  HTML report with exon sequences [Default: products.tsv]",
                           )
        group.add_argument("-d",
                           "--rdsFile",
                           dest="rdsFile",
                           help="A filename for the RDS object of the result from the `designPrimers` R function "
                                "[Default: result.rds]",
                           )
        group.add_argument("-s",
                           "--sep",
                           dest="sep",
                           help="The separator in input and output files [Default: \\t]",
                           )

        args = parser.parse_args(sys.argv[2:])

        # start the primer module

        # make sure we can load the sub module
        sys.path.append(os.path.join(os.path.dirname(__file__)))

        import primer.primer_r
        primer_instance = primer.primer_r.PrimerDesign(args, program_name, version)
        primer_instance.run_module()

    @staticmethod
    def detect():
        parser = argparse.ArgumentParser(
            description="circular RNA detection")
        # NOT prefixing the argument with -- means it"s not optional
        parser.add_argument("-C",
                            "--params",
                            dest="cli_params",
                            help="Defines the input parameters for DCC",
                            default="--help"
                            )
        args = parser.parse_args(sys.argv[2:])

        import os
        os.system("DCC " + args.cli_params)

    @staticmethod
    def reconstruct():
        parser = argparse.ArgumentParser(
            description="circular RNA reconstruction")
        # NOT prefixing the argument with -- means it"s not optional
        parser.add_argument("-C",
                            "--params",
                            dest="cli_params",
                            help="Defines the input parameters for DCC",
                            default="--help"
                            )
        args = parser.parse_args(sys.argv[2:])

        import os
        os.system("FUCHS " + args.cli_params)

if __name__ == "__main__":
    main()
