#iverilog -o a.out -g2005-sv DUT.v testbench.sv dut_if.sv
svseed=`python randomizer.py`
vvp a.out +svseed=$svseed

echo $svseed
python vcd_parser.py "vcd/dump.$svseed.vcd" "$svseed"
