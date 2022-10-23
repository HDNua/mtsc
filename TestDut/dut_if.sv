interface dut_if #(parameter
BW_QUERY_DATA = 32,
END = 0
) (
input       wire    iClk,
input       wire    iRsn
);

logic                           checker_start;
logic                           checker_end;
logic[BW_QUERY_DATA-1:0]        checker_rtl;
logic[BW_QUERY_DATA-1:0]        checker_lls;


//
logic   checker_run;
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        checker_run = 0;
    end
    else if (checker_start) begin
        checker_run = 1;
    end
    else if (checker_end) begin
        checker_run = 0;
    end
end

//
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin

    end
    else if (checker_run) begin
        if (checker_rtl == checker_lls) begin
`ifdef PRINT            
            $display("SUCCESS! value matches at time %0d ns",
                $time);
`endif
        end
        else begin
`ifdef PRINT            
            $display("ERROR! differ value; RTL(%0d) vs LLS(%0d) at time %0d ns",
                checker_rtl, checker_lls, $time);
`endif
        end
    end
end

//
always @(*) begin
    checker_lls = checker_rtl;
end



endinterface