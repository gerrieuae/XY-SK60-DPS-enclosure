# 36 V Bench Power Supply Enclosure

A 3D-printed enclosure for a 36 V / 5 A bench power supply, modelled in SolidCraft.
Inside: an AC-DC2416 open-frame supply, an XY-SK60 controller with display, a front mains rocker switch, a Schurter C14 inlet with fuse and switch, three 4 mm banana sockets, and a 5 V fan powered by an LM2596HV buck module.

**Size:** 110 × 150 × 85 mm. It prints in two halves that snap together with 6 clips and need no screws.

The full design specification is in **[spec.md](spec.md)**: dimensions, positions, wiring, clearances and open items.

## Files

| File | What it is |
|---|---|
| `PSU_Enclosure_110x85.sc` | **Main design.** Enclosure plus all components, parametric |
| `Enclosure_Top.3mf`, `Enclosure_Bottom.3mf` | Print-ready halves, exported from the main design |
| `AC-DC2416.sc` | AC-DC supply model (board, heatsinks, terminals, wiring keep-out spaces) |
| `XY-SK60.sc` | Controller model (bezel, body, tabs, heatsink, rear connectors) |
| `C14_Schurter_KM00-1205-11.sc` | IEC inlet, imported from the vendor STEP |
| `Rocker_Switch.sc` | Mains rocker switch |
| `Banana_ST351B_Black/Red/Green.sc` | 4 mm banana sockets |
| `iec-v14-wide.sc` | Earlier sketch of a Qualtek 764-00/002 inlet (not used) |
| `PSU_Enclosure.sc` | Older layout v2 (145 × 125 × 90), kept for reference |
| `oldTry/` | Source STEP files (fan, LM2596, banana socket), fan datasheet values and the first scripted attempt |

## Printing

| Part | Orientation |
|---|---|
| `Enclosure_Bottom.3mf` | Upright, so the clip arms print vertically and can flex |
| `Enclosure_Top.3mf` | Upside down, lid on the bed |

- **Material:** PETG, or ASA for more heat margin.
- **Settings:** 2.5 mm walls; no supports needed.

## Assembly notes

- **Fan supply:** set the LM2596HV output to **5.0 V** before connecting the fan.
- **Mains switching:** the front rocker switches the mains, and the IEC module's switch on the back also works.
- **Earth:** bond the green ⏚ banana to mains earth (PE).
- **Wire slack:** wires cross the split at Z 23, so leave enough slack to open the case.
- **Mains safety:** the AC-DC2416 is open-frame, so the inside is **live when plugged in**. Build and test with mains-safety precautions.

## Editing the design

- **Parameters:** open `PSU_Enclosure_110x85.sc` in SolidCraft. The main parameters (`enc_w`, `enc_d`, `enc_h`, `ctl_z`, `slot_bridge`, …) are listed in [spec.md §7](spec.md#7-parameters-main-ones-in-psu_enclosure_110x85sc).
- **Changing the box size:** many feature positions are fixed numbers, so changing only the box size will not move the standoffs, vents or clips.

## Credits

The models of the fan (Pelonis, via TraceParts), the LM2596 module, the ST-351B banana socket and the Schurter inlet come from their makers' or contributors' STEP files and remain theirs. Check their licences before publishing this repository.
