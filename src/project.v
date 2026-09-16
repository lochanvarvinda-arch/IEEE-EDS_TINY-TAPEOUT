`default_nettype none

module tt_um_lochanvarvinda_arch (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  reg [7:0] shift_reg;

  always @(posedge clk) begin
    if (!rst_n)
      shift_reg <= 8'b0;
    else if (ui_in[1])
      shift_reg <= {shift_reg[6:0], ui_in[0]};
  end

  assign uo_out = shift_reg;
  assign uio_out = 8'b0;
  assign uio_oe = 8'b0;

  wire _unused = &{ena, uio_in, 1'b0};

endmodule
