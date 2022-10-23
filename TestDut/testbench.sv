`timescale 1ns/1ns

module testbench #(parameter
BW_QUERY_DATA = 32,
END = 0
);
reg     rClk;
reg     rRsn;
wire    wEnd;

int     svseed;
reg unsigned[31:0]          delay0;
reg unsigned[31:0]          delay1;
reg unsigned[31:0]          delay2;

reg                         rDutStart;
wire                        wSlotTick;

reg                         rQueryDataEn;
reg[BW_QUERY_DATA-1:0]      rQueryData;

wire[BW_QUERY_DATA-1:0]     wQueryData;
wire                        wQueryEnd;

string  dump_name;


//
dut_if #(
.BW_QUERY_DATA          (BW_QUERY_DATA)
) dut_if0 (
.iClk           (rClk),
.iRsn           (rRsn)
);

//
DUT #(
.BW_QUERY_DATA          (BW_QUERY_DATA)
) A_DUT (
.iClk           (rClk),
.iRsn           (rRsn),

.iStart         (rDutStart),
.oSlotTick      (wSlotTick),

.iQueryDataEn   (rQueryDataEn),
.iQueryData     (rQueryData),

.oQueryData     (wQueryData),
.oQueryEnd      (wQueryEnd),

.oEnd           (wEnd)
);

//
assign dut_if0.checker_start = A_DUT.iQueryDataEn;
assign dut_if0.checker_end = A_DUT.oQueryEnd;
assign dut_if0.checker_rtl = A_DUT.oQueryData;


//
always begin
#2          rClk = ~rClk;
end


initial begin
            $value$plusargs("svseed=%0d", svseed);
            $display("svseed is %0d", svseed);

            dump_name = $sformatf("vcd/dump.%0d.vcd", svseed);
            $display("dump_name is [%0s]", dump_name);

            //$srandom(svseed);
            delay0 = $urandom(svseed) % 1000000;

            $dumpfile(dump_name);

            //$dumpvars;

            $dumpvars(0, rQueryData);
            $dumpvars(1, dut_if0.checker_start);
            $dumpvars(1, dut_if0.checker_end);
            $dumpvars(1, dut_if0.checker_run);
            $dumpvars(1, dut_if0.checker_rtl);
            $dumpvars(1, dut_if0.checker_lls);

            rClk = 0; rRsn = 1;
#10         rRsn = 0;
#2          rRsn = 1;

#4500000    
            $display("svseed is %0d", svseed);
            $finish;
end

initial begin
            rDutStart = 0;
#delay0     rDutStart = 1;
            @(posedge rClk);
#1          rDutStart = 0;

end

initial begin
            rQueryDataEn = 0;
#10         wait (rDutStart == 1);
            $display("dut started;");

            //
            repeat (3) begin
                delay1 = $urandom(svseed) % 100000;
#delay1         rQueryDataEn = 1; rQueryData = $urandom % 30 + 1;

                @(posedge rClk);
#1              rQueryDataEn = 0;

                @(posedge wSlotTick);

            end
end


endmodule
