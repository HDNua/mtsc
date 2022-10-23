module DUT #(parameter
BW_QUERY_DATA = 4,
BW_SESSION = 32,
BW_CLOCK_COUNT = 32,
BW_SLOT_INDEX = 32,
END = 0
) (
input   wire        iClk,
input   wire        iRsn,

input   wire                            iStart,

output  wire                            oSlotTick,

input   wire                            iQueryDataEn,
input   wire[BW_QUERY_DATA-1:0]         iQueryData,

output  wire[BW_QUERY_DATA-1:0]         oQueryData,
output  wire                            oQueryEnd,

output  wire                            oEnd
);
localparam CLOCK_COUNT_1TTI = 250000;

reg[BW_SESSION-1:0]         rSession;
reg[BW_CLOCK_COUNT-1:0]     rClockCount;
reg                         rSlotTick;
reg[BW_SLOT_INDEX-1:0]      rSlotIndex;

//
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        rSession <= 0;
    end
    else if (iStart) begin
        rSession <= rSession + 1;
    end
end

//
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        rClockCount <= 0;
    end
    else if (iStart) begin
        rClockCount <= 0;
    end
    else if (rSession == 0) begin
        rClockCount <= 0;
    end
    else if (rClockCount == CLOCK_COUNT_1TTI) begin
        rClockCount <= 0;
    end
    else begin
        rClockCount <= rClockCount + 1;
    end
end

//
assign rSlotTick = iStart || (rClockCount == CLOCK_COUNT_1TTI);
assign oSlotTick = rSlotTick;

//
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        rSlotIndex <= 0;
    end
    else if (iStart) begin
        rSlotIndex <= 0;
    end
    else if (rSession == 0) begin
        rSlotIndex <= 0;
    end
    else if (rClockCount == CLOCK_COUNT_1TTI) begin
        rSlotIndex <= rSlotIndex + 1;
    end
end

//
reg[BW_QUERY_DATA-1:0] rQueryData;
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        rQueryData <= 0;
    end
    else if (iQueryDataEn) begin
        rQueryData <= iQueryData;
    end
    else if (rQueryEnd) begin
        rQueryData <= 0;
    end
    else if (rQueryData[0] == 0) begin
        rQueryData <= rQueryData[BW_QUERY_DATA-1:1];
    end
    else if (rQueryData != 1) begin
        rQueryData <= 3 * rQueryData + 1;
    end
end
assign oQueryData = rQueryData;

//
reg rQueryEnd;
always @(posedge iClk or negedge iRsn) begin
    if (!iRsn) begin
        rQueryEnd <= 0;
    end
    else if (rQueryData == 0) begin
        rQueryEnd <= 0;
    end
    else if (rQueryEnd) begin
        rQueryEnd <= 0;
    end
    else if (iQueryDataEn) begin
        rQueryEnd <= (rQueryData == 1);
    end
    else if (rQueryData <= 2) begin
        rQueryEnd <= 1;
    end
end
assign oQueryEnd = rQueryEnd;

endmodule