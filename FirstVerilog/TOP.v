module TOP #(parameter
BW_DATA=32
) (
input  wire[32-1:0] iData,
output wire[32-1:0] oData
);

    assign oData = iData;
    
endmodule