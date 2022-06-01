#!/bin/bash

set -e

echo "Exporting conda environment..."
conda env export -p conda | awk -F= '
    BEGIN {
        mode = "chn";
    }
    /^(prefix|name):/ {
        next;
    }
    /^dependencies:$/ {
        mode = "dep";
        for (i = chn_idx - 1; i >= 0; ) {
            print chn_arr[i--];
        }
    }
    /- (cudatoolkit|cudnn|scglue)/ {
        print "# "$0;
        next;
    }
    /^[^=]+=[^=]+=[^=]+$/ {
        print $1"="$2;
        next;
    }
    /- .+$/ {
        if (mode == "chn") {
            if ($0 !~ /defaults/) {
                chn_arr[chn_idx++] = $0;
            }
            next;
        }
    }
    /^variables:$/ {
        mode = "var";
    }
    {
        if (mode != "var") {
            print $0;
        }
    }
' > conda.new.yaml
if diff -y --suppress-common-lines conda.new.yaml conda.yaml; then
    rm conda.new.yaml
    echo "* Environment not changed."
else
    mv conda.new.yaml conda.yaml
    echo "* Environment file written to '$(pwd)/conda.yaml'."
fi

# echo -e "\nExporting renv environment..."
# Rscript -e "renv::snapshot()"