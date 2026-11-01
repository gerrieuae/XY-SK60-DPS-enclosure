# Bench Power Supply — Design Specification

**Project:** 36 V / 5 A benchtop DC power supply in a 3D-printed enclosure
**Designer:** Gerrie
**CAD tool:** SolidCraft 0.25.1 (parametric `.sc`)
**Current design file:** `PSU_Enclosure_110x85.sc`
**Revision:** v3, 2026-11-01. Replaces the 2026-10-28 spec (165 × 178 × 75 box with banana columns beside the display).
**Status:** Model complete, split for printing, no interference. A few dimensions still need checking before the first print (see §8).

---

## 1. Overview

A mains-powered bench supply. An open-frame AC-DC module makes 36 V DC. An XY-SK60 buck controller on the front panel sets and displays the output voltage and current. The output goes to three 4 mm banana sockets. A 50 mm fan under the lid draws air in through the floor and blows it out through the top.

```
FRONT (seen from the front)                 REAR (seen from the back)
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│ ┌────────────────────────┐       │        │  ┌─────┐    ┌──────────────┐     │
│ │      XY-SK60 display   │  [▮]  │        │  │LM2596│   │  IEC  C14    │     │
│ │  81.6 × 40.6 cutout    │ mains │        │  │(inside)  │ inlet+fuse+sw│     │
│ └────────────────────────┘ rocker│        │  └─────┘    └──────────────┘     │
│ ──────── seam (Z 23) ──────────  │        │ ──────── seam (Z 23) ──────────  │
│      ⊙ −      ⊙ +      ⊙ ⏚       │        │                                  │
└──────────────────────────────────┘        └──────────────────────────────────┘
        black    red     green

TOP VIEW (front at the bottom)
┌──────────────────────────────────┐  rear wall: IEC inlet (right), LM2596 (left, inside)
│  DC out ▲                        │
│  ┌────────────────────────┐      │
│  │ AC-DC2416, rotated 90° │ fan  │  fan 50×50 under the lid, over the transformer
│  │ (long axis front–back) │      │
│  │ AC in ▼                │      │
│  └────────────────────────┘      │
│  XY-SK60 body (45 deep)  rocker  │  front wall
└──────────────────────────────────┘
```

### Coordinate system (used throughout)
Origin at the centre of the outer bottom face. **X** = width (+X is right, seen from the front). **Y** = depth (−Y is the front panel). **Z** = height (0 is the floor).

---

## 2. Enclosure

| Property | Value |
|---|---|
| Outer size (W × D × H) | **110 × 150 × 85 mm**, in 5 mm steps |
| Wall / lid thickness | 2.5 mm / 2.5 mm (the lid is part of the top half) |
| Vertical corner radius | 5 mm outside, 2.5 mm inside |
| Material | PETG, or ASA for more heat margin (heat deflection about 75 °C vs 98 °C) |
| Printer | Bambu Lab P1S (FDM) |
| Feet | 4 × Ø4 mm holes, 10 mm in from each corner, for M4 or stick-on rubber feet |

### 2.1 Split, lip and seam
| Feature | Value |
|---|---|
| Split plane | Horizontal at **Z 23**, between the banana row and the display |
| `Enclosure_Bottom` | Z 0–23, plus a lip to Z 26 and clip arms to Z 33 |
| `Enclosure_Top` | Z 23–85, including the lid, the front and rear panel cut-outs, and the fan mount |
| Lip (on the bottom) | 1.2 thick × 3 high, on the inner half of the wall |
| Groove (in the top) | 0.2 mm clearance around the lip, 3.4 deep |
| Seam | 0.6 mm chamfer on both outer edges, which forms a neat V-groove |

### 2.2 Snap clips (6, no screws)
| Property | Value |
|---|---|
| Positions | Left and right walls at Y −64 and Y +54; front wall at X 43 (behind the rocker); rear wall at X 25 (under the IEC inlet) |
| Arm | 1.2 × 6 mm, Z 13–33, about 12 mm free to flex, part of the bottom half |
| Hook | Sticks 0.8 mm into the wall. Ramped top for lead-in; retention face about 70° |
| Pocket | Blind pocket on the inside of the top's wall, 7 wide, Z 29.3–32.7. Not visible from outside |
| Release | Pull firmly, or press the arm through a vent slot |

### 2.3 Ventilation (floor in → lid out, fan assisted)
All slots are **2 mm wide** (a 2.5 mm test probe cannot enter). No slot is longer than **20 mm**; longer runs are split by **3 mm bridges** (parameter `slot_bridge`).

| Group | Where | Slots |
|---|---|---|
| Fan grille | Lid, over the fan | 9 × (2 × 18.5) |
| Lid vents, front | Lid, Y −45.5 to −31.5 (above the controller's heatsink) | 16 × 14 |
| Lid vents, rear | Lid, Y 26.5 to 46.5 | 16 × 20 |
| Floor vents, front | Floor, Y −70.5 to −63 | 20 × 7.5 |
| Floor vents, right | Floor, X 36–50, Y −52.5 to 47.5 | 4 × (5 × 17.6) |
| Floor vents, left | Floor, X −50 to −36, Y −27.5 to 47.5 | 4 × (4 × 16.5) |

### 2.4 Panel cut-outs
| Feature | Panel | Centre (X, Z) | Size |
|---|---|---|---|
| XY-SK60 controller | Front | (−7, 55) | 81.6 × 40.6 rectangle, plain (press-fit tabs) |
| Mains rocker switch | Front | (43, 55), height linked to the display (`sw_z = ctl_z`) | 8.0 × 13.2 (**to verify**) |
| Banana − (black) | Front | (−26, 14) | Ø6 |
| Banana + (red) | Front | (−7, 14) | Ø6 |
| Banana ⏚ (green) | Front | (12, 14) | Ø6 |
| IEC inlet | Rear | (25, 52) | 47.4 × 28.4 rectangle |
| Fan screws | Lid | fan centre ±20 | 4 × Ø3.4 |

### 2.5 Internal mounts
| Mount | Position | Size |
|---|---|---|
| PSU standoffs (4) | (−27.35, −57.9), (28.35, −57.9), (−27.35, 47.7), (28.35, 47.7) | Ø8 × 5 high, Ø3.5 hole |
| LM2596 standoffs (2) | Rear wall inside, at (X −28, Z 35.87) and (X −11, Z 69.05) | Ø6 × 5 long, Ø2.5 hole (M3 self-tapping) |

---

## 3. Components

| # | Part | Model file | Position / notes |
|---|---|---|---|
| 1 | **AC-DC2416 Rev D**: 36 V 5 A 180 W open-frame supply (Amazon B09CZCHZP7) | `AC-DC2416.sc` | Rotated 90° (long axis front–back); AC terminal at front left, DC terminal at the rear. PCB centre (0.5, −5.1), on 5 mm standoffs |
| 2 | **XY-SK60** buck controller with display (measured; SK60X size) | `XY-SK60.sc` | Front, centre (−7, 55) |
| 3 | **Mains rocker switch**, 2-pin | `Rocker_Switch.sc` | Front, right of the display; switches the mains |
| 4 | **Schurter KM00.1205.11**: C14 inlet with fuse holder and switch | `C14_Schurter_KM00-1205-11.sc` (from the vendor STEP) | Rear right, horizontal, its switch on the right seen from the front |
| 5 | **ST-351B 4 mm banana sockets** × 3 (black / red / green) | `Banana_ST351B_*.sc` | Front, under the display, 19 mm pitch |
| 6 | **Pelonis C5010H05BPLP1b-7** fan: 50 × 50 × 10, 5 V, 0.27 A, 13.6 CFM | from `oldTry/DC5010_7.stp` | Under the lid, centre (0.5, −2.5), blowing upward, over the transformer |
| 7 | **LM2596HV buck module** (for the fan's 5 V) | from `oldTry/LM2596_DC-DC_CONVERTER.STEP` | Rear wall inside, left of the IEC inlet, vertical; input at the bottom, output at the top |

### 3.1 AC-DC2416 (measured 2026-10-31, heights above the top of the 1.6 mm PCB)
| Property | Value |
|---|---|
| Board | 114.8 × 65.5 mm; M4 holes at 105.6 × 55.7 |
| Terminal blocks | 8.5 mm; wires come in with spade connectors from the PCB edge |
| Transformer | 28.5 mm |
| Heatsinks (primary and secondary) | 24.5 mm |
| Bulk capacitor | 27 mm |
| Source | Datasheet `XX-DC2416_datasheet_Rev_C_D.pdf` (Robu), plus measurements |

### 3.2 XY-SK60 (measured)
| Property | Value |
|---|---|
| Bezel | 86 × 45 |
| Body | 81 × 40, 45 deep behind the panel |
| Panel cut-out | 81.6 × 40.6 (`body_clr` 0.3) |
| Fixing | 4 press-fit ramp tabs on the left and right sides only (7.7 wide, 20 mm apart); none on top or bottom |
| Heatsink | 15.25 tall, fins run left–right, inside the case |
| Rear terminal (seen from the back, left → right) | VIN+, VIN−, OUT−, OUT+; wires leave toward the rear |
| Rear plugs | Temperature probe (2-pin, 2 mm pitch) at the top left; fan (2-pin, 2 mm) and a 4-pin 1 mm plug at the right end |

---

## 4. Wiring

```
Mains ─► IEC C14 (fuse + switch) ─► front rocker ─► AC-DC2416 AC in
                       PE ─────────────────────────────► green banana ⏚ (and PSU earth, if it has one)
AC-DC2416 DC out (36 V) ─┬─► XY-SK60 VIN+ / VIN−
                         └─► LM2596HV in ─► 5.0 V ─► fan (wires fixed, routed along the top)
XY-SK60 OUT+ / OUT− ─► red (+) / black (−) bananas
```

- The front rocker switches the **mains**. The IEC module's own switch on the back also works.
- **Set the LM2596HV to 5.0 V before connecting the fan.** The standard LM2596 is rated only to 40 V input, which is too close to 36 V; use the HV (60 V) version.
- The mains, the DC and the fan-converter input wires all cross the split at Z 23. Leave enough slack to open the case.
- Treat the inside as live when plugged in: the PSU is open-frame. Keep ≥ 6 mm between mains parts and the DC wiring.

---

## 5. Clearances (checked in the model, 2026-11-01)

No parts overlap. The tightest spots:

| Pair | Gap |
|---|---|
| PSU bulk capacitor ↔ controller capacitor C1 | **0.9 mm** (vertical). If your bulk capacitor is taller than 27 mm, raise `ctl_z` |
| Controller wiring space ↔ PSU transformer | 1.9 mm |
| Controller case ↔ inner lid | 7.5 mm |
| Bezel top ↔ top edge of the case | 7.5 mm |

---

## 6. Printing

| Part | Orientation | Notes |
|---|---|---|
| `Enclosure_Bottom.3mf` | Upright (floor on the bed) | The clip arms then print vertically, along the layer direction, so they can flex |
| `Enclosure_Top.3mf` | Upside down (lid on the bed) | The panel cut-outs bridge cleanly |

- Print one clip as a test piece first. Tune the hook depth (0.8) or the arm thickness (1.2) for your filament.
- For long use near full load, ASA is the safer material.

---

## 7. Parameters (main ones in `PSU_Enclosure_110x85.sc`)

| Name | Value | Meaning |
|---|---|---|
| `enc_w` / `enc_d` / `enc_h` | 110 / 150 / 85 | Outer size |
| `wall`, `lid_t`, `corner_r` | 2.5, 2.5, 5 | Shell |
| `ctl_x`, `ctl_z` | −7, 55 | Controller centre |
| `sw_x`, `sw_z` | 43, = `ctl_z` | Rocker centre |
| `iec_x`, `iec_z` | 25, 52 | IEC inlet centre |
| `ban_z`, `ban_pitch`, `ban_hole_d` | 14, 19, 6 | Banana row |
| `fan_x`, `fan_y`, `fan_hole_pitch` | 0.5, −2.5, 40 | Fan |
| `slot_w`, `slot_bridge` | 2, 3 | Vents |
| `split_z`, `lip_t`, `lip_h`, `lip_clr`, `seam_ch` | 23, 1.2, 3, 0.2, 0.6 | Split |

> Many feature positions (standoffs, vents, clips, the lip sketch) are fixed numbers, not linked to `enc_d` or `enc_w`. Changing the box size alone will not move them. Check those features after a size change.

---

## 8. Open items

| # | Item | Status |
|---|---|---|
| 1 | Measure the rocker switch flange and body; confirm the 8.0 × 13.2 cut-out (the listing's 15 × 9 doesn't match its own drawing) | ⏳ |
| 2 | Schurter snap tabs sit 1.4–3.4 mm behind the flange; check that they lock on a 2.5 mm wall | ⏳ |
| 3 | The banana lug sits partly inside the wall in the model; check on the real part | ⏳ |
| 4 | Confirm the bulk capacitor is no taller than 27 mm (0.9 mm gap to the controller) | ⏳ |
| 5 | Print a test clip; tune the hook and arm for PETG or ASA | ⏳ |
| 6 | Use the XY-SK60 temperature probe (on the PSU heatsink?) and its fan output | ⏳ |
| 7 | Layout, size, split, clips, vents, fan and fan supply | ✅ |

---

## 9. History

| Date | Change |
|---|---|
| 2026-10-28 | First spec: 165 × 178 × 75, banana columns beside the display, IEC centred at the rear (`oldTry/`) |
| 2026-10-31 | Layout v2 `PSU_Enclosure.sc`: 145 × 125 × 90; outer sizes in 5 mm steps |
| 2026-10-31 | Layout v3: 110 × 170 × 80; PSU rotated, bananas under the display, IEC at the rear right, front mains rocker, fan, LM2596HV |
| 2026-10-31 | Split into top and bottom with a lip, seam chamfer and 6 clips |
| 2026-11-01 | Depth 170 → 150 (controller raised to Z 55), height 80 → 85, rocker aligned with the display, slot bridges (max 20 mm) |
