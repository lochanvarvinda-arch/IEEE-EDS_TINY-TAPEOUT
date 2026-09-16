## How it works

This project implements an 8-bit serial-in, parallel-out shift register.
On each rising edge of `clk`, if `rst_n` is low the register clears to zero.
Otherwise, if `ui_in[1]` (SHIFT_EN) is high, the register shifts left by one bit,
loading `ui_in[0]` (SERIAL_IN) into the least significant bit. The full 8-bit
register value is continuously output on `uo_out`.

## How to test

1. Assert `rst_n` low for at least one clock cycle to reset the register to 0.
2. Release `rst_n` (set high).
3. Set `ui_in[1]` = 1 to enable shifting, and drive `ui_in[0]` with the serial
   bit you want to shift in.
4. On each clock edge, `uo_out` will shift left, inserting `ui_in[0]` at bit 0.
5. Set `ui_in[1]` = 0 to hold the current value without shifting.
