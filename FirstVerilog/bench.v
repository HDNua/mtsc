`timescale 1ns/1ps


module bench;

    reg[31:0] rData;
    wire[31:0] wData;

    reg        iClk;

    always begin
        #2 iClk = ~iClk;
    end

    TOP A_TOP(
        .iData(rData),
        .oData(wData)
    );

    initial begin
        iClk = 0;

        $dumpfile("test.vcd");
        $dumpvars;
            rData = 0;
#10         rData = 10;
#10         rData = 20;
#10         rData = 30;
#10         rData = 40;
#10         rData = 50;
#4000000    $finish;
    end

endmodule