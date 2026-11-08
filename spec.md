# Bench Power Supply — Design Specification

**Project:** 36 V / 5 A benchtop DC power supply in a 3D-printed enclosure
**Designer:** Gerrie
**CAD tool:** SolidCraft 0.25.1 (parametric `.sc`)
**Current design file:** `PSU_Enclosure_120x85.sc`
**Revision:** v3.1, 2026-11-01. Parametric rework of v3 (same geometry at 120 × 150 × 85). Replaces the 2026-10-28 spec (165 × 178 × 75 box with banana columns beside the display).
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
│      ⊙ −      ⊙ ⏚      ⊙ +       │        │                                  │
└──────────────────────────────────┘        └──────────────────────────────────┘
        black   green     red     (NEG / EARTH / POS labels above the seam)

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
| Outer size (W × D × H) | **120 × 150 × 85 mm**, in 5 mm steps |
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
| Lip (on the bottom) | 1.2 thick × 3 high (`lip_t`, `lip_h`), on the inner half of the wall |
| Groove (in the top) | 0.2 mm clearance (`lip_clr`) outside the lip and 0.3 above it, 3.4 deep |
| Construction | No split or join features. `Copy_Bottom` copies the finished box; `Bottom_Cut_Above` (an oversize box) removes everything above `split_z + lip_h`, and `Bottom_Outer_Trim` (thin extrude of `Sk_Lip`, from `split_z` up) removes the outer half of the wall above `split_z`, which leaves the lip. On the original, `Top_Cut_Below` removes everything below `split_z` and `Groove` cuts the lip clearance. Every tool face lies far outside the body or inside material, so no boolean has coplanar faces; this rebuilds without warnings and the seam lies exactly at Z 23 (the earlier two-split version nudged the split tool by 4 µm / 2 µrad and warned). `Split_Plane` and `Lip_Top_Plane` are kept for reference only |
| Seam | 0.6 mm chamfer on both outer edges, which forms a neat V-groove |

### 2.2 Snap clips (6, no screws)
| Property | Value |
|---|---|
| Positions | Left and right walls at Y −64 and Y +54 (`clip_y_front = −(enc_d/2 − 11)`, `clip_y_rear = enc_d/2 − 21`); front wall at X 44.5 (`clip_x_front = sw_x`, behind the rocker); rear wall at X 25 (`clip_x_rear = iec_x`, under the IEC inlet) |
| Arm | `clip_arm_t` × `clip_w` = 1.2 × 6 mm, from `clip_z0 = split_z − 10` up 20 (`clip_arm_h`), about 12 mm free to flex, part of the bottom half |
| Hook | Sticks 0.8 mm (`clip_hook`) into the wall from `clip_hook_z = split_z + 6.1`. Ramped top for lead-in; retention face about 70° |
| Pocket | Blind pocket on the inside of the top's wall, `clip_pocket_w` = 7 wide, from `clip_pocket_z = split_z + 6.3`, 3.4 high (`clip_pocket_h`). Not visible from outside |
| Release | Pull firmly, or press the arm through a vent slot |

### 2.3a Clip test box (`clipTest.sc`)

A small box to print before the full enclosure, to tune the clips for the filament. It is built from the same features as the main design (shell, `Copy_Bottom` / box cuts, lip, groove, seam chamfer and all 6 clips), with the components, cut-outs, vents, posts and labels left out.

| Property | Value |
|---|---|
| Size | 40 × 50 × 28 (`enc_w`, `enc_d`, `enc_h`) |
| Split | Z 13 (`split_z`), so `clip_z0` = 3 sits just above the 2.5 mm floor |
| Clips | Same arm, root, hook and pocket as §2.2; front and rear clips centred (`clip_x_front` = `clip_x_rear` = 0), side pairs at Y −14 and +4 |
| Files | `clipTest.sc`, `clipTest_Top.3mf`, `clipTest_Bottom.3mf` (printed like the main halves, §6) |
| Tuning | Change `clip_hook`, `clip_arm_t` or `clip_pocket_*` in `clipTest.sc`, reprint, then copy the values that work into `PSU_Enclosure_120x85.sc` |

### 2.3b Insert test (`insertTest.sc`)

Four standoffs like the PSU ones, to find the hole size that holds the M3 heat-set inserts (Ø5 × 4 long) best before printing the enclosure.

| Property | Value |
|---|---|
| Standoffs | 4 × Ø9 × 5 high (`boss_d`, `boss_h`) on a 56 × 24 × 2.5 plate, 14 mm apart |
| Holes | Ø3.9, 4.0, 4.1 and 4.2, 5 deep (blind), each with the 1 mm lead-in chamfer (`insert_ch`); the size is recessed into the plate in front of each standoff |
| Files | `insertTest.sc`, `insertTest.3mf` (flat on the bed) |
| Use | Press an insert into each hole; pick the one that goes in flush, square and does not spin when you tighten an M3 screw. Set `psu_boss_hole` and `lm_boss_hole` in `PSU_Enclosure_120x85.sc` to that size (now 4.2, the size that tested best). Change `ins_hole` / `hole_step` in `insertTest.sc` to test other sizes |

### 2.3 Ventilation (floor in → lid out, fan assisted)
All slots are **2 mm wide** (`slot_w`; a 2.5 mm test probe cannot enter) on a 4 mm pitch (`vent_pitch`). No slot is longer than **20 mm** (`vent_len_max`); longer runs are split by **3 mm bridges** (`slot_bridge`). The slot counts follow the box: the lid and front floor fields are centred and get `floor((enc_w − 2·margin)/vent_pitch) + 1` slots, the side floor runs span `enc_d` minus their front and rear margins and are cut into `ceil(run / vent_len_max)` segments. The fan grille and the lid vent fields are placed from the fan (`fan_x`, `fan_y`, `fan_s`). The table below is at 120 × 150 × 85.

| Group | Where | Slots |
|---|---|---|
| Fan grille | Lid, over the fan | 9 slots, each split by a 3 mm bridge; they end inside the Ø44 fan circle (`fan_grille_r` 22), so the middle five are 2 × 18.5 and the outer ones shorter (2 × 16.2 and 2 × 12.5) |
| Lid vents, front | Lid, Y −45.5 to −31.5 (above the controller's heatsink) | 16 × 14 |
| Lid vents, rear | Lid, Y 26.5 to 46.5 | 16 × 20 |
| Floor vents, front | Floor, Y −70.5 to −63 | 20 × 7.5 |
| Floor vents, right | Floor, X 36–50, Y −52.5 to 47.5 | 4 × (5 × 17.6) |
| Floor vents, left | Floor, X −50 to −36, Y −27.5 to 47.5 | 4 × (4 × 16.5) |

### 2.4 Panel cut-outs
| Feature | Panel | Centre (X, Z) | Size |
|---|---|---|---|
| XY-SK60 controller | Front | (−9, 55) | 81.6 × 40.6 rectangle, plain (press-fit tabs) |
| Mains rocker switch | Front | (44.5, 55), height linked to the display (`sw_z = ctl_z`) | 19.2 × 13 (KCD1-101 datasheet) |
| Banana − (black) | Front | (−25, 14) = (`ban_x − ban_pitch`, `ban_z`) | Ø8 |
| Banana ⏚ (green) | Front | (0, 14) = (`ban_x`, `ban_z`) | Ø8 |
| Banana + (red) | Front | (25, 14) = (`ban_x + ban_pitch`, `ban_z`) | Ø8 |
| Socket labels | Front, top half | NEG, EARTH, POS centred over the sockets, baseline `label_z` = 26 (above the seam chamfer, below the display bezel at Z 32.5) | Arial Bold, capital height `label_h` = 0.8 × `name_h` = 3.76, recessed `name_depth` = 0.3 (`label_neg`, `label_earth`, `label_pos`) |
| Rocker label | Front, top half | MAINS centred over the rocker, baseline `mains_z` = `sw_z + 13` = 68 (above the 15 × 21 bezel, which ends at Z 65.5) | as the socket labels (`label_mains`) |
| IEC inlet | Rear | (25, 52) | 48.1 × 28.1 rectangle (`iec_cut_w` × `iec_cut_h`: 47.5 × 27.5 part + 0.3 per side) |
| Fan screws | Lid | fan centre ±20 | 4 × Ø3.4, 90° countersink Ø6.8 on the top (`fan_csk_d`) for M3 countersunk screws |
| Name | Lid, outside | centred in X, baseline `name_front` = 10 mm behind the front wall | `name_text` = "cREATRON DPS XY-SK60X", Arial Bold, capital height `name_h` = 4.7 mm (about 85 mm wide, 71 % of `enc_w`), recessed `name_depth` = 0.3 mm (one first layer when printed lid-down). Reads correctly from the front |

### 2.5 Internal mounts
| Mount | Position | Size |
|---|---|---|
| PSU standoffs (4) | `psu_x` ± `psu_hole_dx`/2, `psu_y` ± `psu_hole_dy`/2 = (−27.35, −44.9), (28.35, −44.9), (−27.35, 60.7), (28.35, 60.7) | Ø9 × 5 high (`psu_boss_d`, `standoff_h`), Ø4.2 × 5 deep blind hole (`psu_boss_hole`) with a 1 mm lead-in chamfer (`insert_ch`) for M3 heat-set inserts (Ø5 × 4 long); M3 screws through the board's M4 holes, with washers |
| LM2596 posts (2) | On the inner rear wall (Y = `enc_d/2 − wall`), at (`lm_x`, `lm_z`) = (−28, 35.87) and (+`lm_hole_dx`, +`lm_hole_dz`) = (−11, 69.05) | Square 9 × 9, 5 long (`lm_boss_w`, `lm_boss_h`), Ø4.2 × 5 deep blind hole (`lm_boss_hole`) with a 1 mm lead-in chamfer (`insert_ch`) for M3 heat-set inserts Ø5 × 4. A 45° gusset on the lid side runs 5 mm up the wall, so the posts print without support when the top is printed lid-down (§6) |

---

## 3. Components

| # | Part | Model file | Position / notes |
|---|---|---|---|
| 1 | **AC-DC2416 Rev D**: 36 V 5 A 180 W open-frame supply (Amazon B09CZCHZP7) | `AC-DC2416.sc` | Rotated 90° (long axis front–back) with the AC terminal at the rear right, under the IEC inlet, and the DC terminal at the front, behind the banana sockets. PCB centre (0.5, 7.9), on 5 mm standoffs |
| 2 | **XY-SK60** buck controller with display (measured; SK60X size) | `XY-SK60.sc` | Front, centre (−9, 55) |
| 3 | **Mains rocker switch** KCD1-101: 15 × 21 flange, 12.9 × 18.8 × 13.2 body, 19.2 × 13 cut-out (datasheet) | `Rocker_Switch_KCD1-101.sc` (`Rocker_Switch_15x21.sc` and the older `Rocker_Switch.sc` are kept but unused) | Front, right of the display; switches the mains |
| 4 | **Schurter KM00.1205.11**: C14 inlet with fuse holder and switch | `C14_Schurter_KM00-1205-11.sc` (from the vendor STEP) | Rear right, horizontal, its switch on the right seen from the front |
| 5 | **ST-351B 4 mm banana sockets** × 3 (black / green / red, left to right). Own model: front cap Ø11.3 × 2.5 with a Ø7.5 nozzle (measured) through the Ø8 panel hole, rear piece Ø11.3 × 4.4 (Ø7.5 bore) behind the panel, metal with Ø7 collar, Ø5.2 thread reaching 14 mm behind the panel inner face (`in_len`, measured) and solder lug | `Banana_4mm_Black/Red/Green.sc` (the vendor-STEP `Banana_ST351B_*.sc` were dropped because their metal body is an open shell; they remain in git history) | Front, under the display, row centred on the box (`ban_x` = 0), 25 mm pitch (`ban_pitch`) so the labels have room |
| 6 | **Pelonis C5010H05BPLP1b-7** fan: 50 × 50 × 10, 5 V, 0.27 A, 13.6 CFM | from `stepFiles/DC5010_7.stp` | Under the lid, centre (0.5, −2.5), blowing upward, over the transformer |
| 7 | **LM2596HV buck module** (for the fan's 5 V) | from `stepFiles/LM2596_DC-DC_CONVERTER.STEP` | Rear wall inside, left of the IEC inlet, vertical; input at the bottom, output at the top |

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

## 5. Clearances (checked in the model, 2026-11-07, PSU turned 180° and 13 mm back)

No parts overlap. The tightest spots:

| Pair | Gap |
|---|---|
| PSU secondary heatsink ↔ controller capacitors | 3.4 mm |
| PSU EMI filter ↔ LM2596 capacitor | 2.2 mm |
| PSU primary heatsink ↔ IEC inlet body | 3.8 mm |
| Controller case ↔ inner lid | 7.5 mm |
| Bezel top ↔ top edge of the case | 7.5 mm |
| Front panel, left → right | 8 mm edge · 86 mm bezel · 3 mm gap · 15 mm switch flange · 8 mm edge (3 mm to each corner radius) |

---

## 6. Printing

| Part | Orientation | Notes |
|---|---|---|
| `Enclosure_Bottom.3mf` | Upright (floor on the bed) | The clip arms then print vertically, along the layer direction, so they can flex |
| `Enclosure_Top.3mf` | Upside down (lid on the bed) | The panel cut-outs bridge cleanly |

- Print the clip test box (`clipTest_Top.3mf`, `clipTest_Bottom.3mf`, §2.3a) first, oriented as above. Tune the hook depth (0.8) or the arm thickness (1.2) for your filament.
- For long use near full load, ASA is the safer material.

---

## 7. Parameters (`PSU_Enclosure_120x85.sc`)

The enclosure is driven by the parameters below (SolidCraft → Parameters). The values shown are the defaults, which reproduce the 120 × 150 × 85 design exactly.

### 7.1 Size and shell

| Name | Value | Meaning |
|---|---|---|
| `enc_w` / `enc_d` / `enc_h` | 120 / 150 / 85 | Outer size. Everything in §7.2 follows these |
| `wall`, `lid_t`, `corner_r` | 2.5, 2.5, 5 | Shell |
| `ctl_x`, `ctl_z` | −9, 55 | Controller centre (the banana cut-outs follow `ctl_x`) |
| `sw_x`, `sw_z`, `sw_cut_w`, `sw_cut_l` | 44.5, = `ctl_z`, 13, 19.2 (KCD1-101 datasheet; add 0.1–0.2 if the printed hole is tight) | Rocker centre and cut-out |
| `iec_x`, `iec_z` | 25, 52 | IEC inlet centre |
| `ban_x`, `ban_z`, `ban_pitch`, `ban_hole_d` | 0, 14, 25, 8 | Banana row: centre X, height, spacing (the socket cut-outs and the NEG / EARTH / POS labels follow; move the socket components by hand after a change) |
| `fan_x`, `fan_y`, `fan_hole_pitch` | 0.5, −2.5, 40 | Fan |
| `slot_w`, `slot_bridge` | 2, 3 | Vents |
| `split_z`, `lip_t`, `lip_h`, `lip_clr`, `seam_ch` | 23, 1.2, 3, 0.2, 0.6 | Split planes (`Split_Plane` at `split_z`, `Lip_Top_Plane` at `split_z + lip_h`), lip, groove and seam (§2.1). The lip and groove sketches are dimensioned from `enc_w`, `enc_d`, `wall`, `corner_r`, `lip_t` and `lip_clr` |
| `standoff_h` | 5 | PSU standoff height |

### 7.2 Derived placement (added 2026-11-01)

| Group | Parameters | Rule |
|---|---|---|
| Feet | `foot_inset` 10, `foot_hole_d` 4 | Ø`foot_hole_d` at `enc_w/2 − foot_inset`, `enc_d/2 − foot_inset` |
| PSU standoffs | `psu_x` 0.5, `psu_y` 7.9, `psu_hole_dx` 55.7, `psu_hole_dy` 105.6, `psu_boss_d` 9, `psu_boss_hole` 4.2 | Four posts at the PSU centre ± half the hole pitch. Move the AC-DC2416 component to (`psu_x`, `psu_y`) when you change these |
| LM2596 posts | `lm_x` −28, `lm_z` 35.87, `lm_hole_dx` 17, `lm_hole_dz` 33.18, `lm_boss_w` 9, `lm_boss_h` 5, `lm_boss_hole` 4.2 | Square posts with a 45° gusset toward the lid, rooted in the inner face of the rear wall, so they follow `enc_d` |
| Lid name | `name_text`, `name_h` 4.7, `name_front` 10, `name_depth` 0.3, `name_y` = `−enc_d/2 + name_front` | Centred text on the lid; `name_h` is not scaled with `enc_w`, so re-check the 60 % coverage after a width change |
| Front labels | `label_neg`, `label_earth`, `label_pos`, `label_mains` (texts), `label_z` 26, `mains_z` = `sw_z + 13`, `label_h` = `name_h * 0.8` | 80 % of the lid name's height, same depth; the socket labels follow `ban_x` and `ban_pitch`, MAINS follows `sw_x` and `sw_z` |
| Fan | `fan_x`, `fan_y`, `fan_s` 50, `fan_hole_pitch` 40, `fan_screw_d` 3.4, `fan_csk_d` 6.8, `grille_l` = `fan_s − 10`, `fan_grille_r` = `fan_s/2 − 3` | Grille slots and screw holes follow the fan. The 9 slots are separate cuts (`Fan_Grille_1A`…`9B`), each as long as `grille_l` allows inside `fan_grille_r`; `grille_n` and `grille_seg` no longer drive them |
| Lid vents | `lid_vent_margin` 30, `lid_vent_gap` 4, `lid_vent_front_l` 14, `lid_vent_rear_l` = `vent_len_max`, `lid_vent_n` | Centred fields, `lid_vent_gap` in front of and behind the fan |
| Floor vents, front | `fv_front_margin` 22, `fv_front_gap` 2, `fv_front_l` 7.5, `fv_front_n` | Centred field just inside the front wall |
| Floor vents, sides | `fv_side_in` 11, `fv_side_clear` 2, `fv_right_n`, `fv_left_n`, `fv_side_rear_margin` 27.5, `fv_right_front_margin` 22.5, `fv_left_front_margin` 47.5, `fv_right_l`, `fv_left_l`, `fv_right_seg`, `fv_left_seg` | Runs along the side walls, split into ≤ `vent_len_max` segments. The slot count per side is what fits between the outer wall and the PSU standoff plus `fv_side_clear` (4 per side at 120 wide, 3 at 110, 2 at 100) |
| Vents, common | `vent_pitch` 4, `vent_len_max` 20, `slot_w` 2, `slot_bridge` 3 | |
| Snap clips | `clip_w` 6, `clip_arm_t` 1.2, `clip_arm_h` 20, `clip_root_h` 8, `clip_z0` = `split_z − 10`, `clip_hook` 0.8, `clip_hook_z` = `split_z + 6.1`, `clip_pocket_w` 7, `clip_pocket_z` = `split_z + 6.3`, `clip_pocket_h` 3.4, `clip_y_front` = `−(enc_d/2 − 11)`, `clip_y_rear` = `enc_d/2 − 21`, `clip_x_front` = `sw_x`, `clip_x_rear` = `iec_x` | All six clips, their hooks and pockets sit on the inner wall faces and follow the split. Each root is 0.1 mm wider on both sides and 0.1 mm lower than its arm, so the arm's faces lie inside the root and the join needs no boolean retry |

### 7.3 What does **not** follow a size change

- The **imported components** (AC-DC2416, XY-SK60, rocker, IEC inlet, bananas, fan, LM2596) are placed by fixed transforms; SolidCraft occurrences take no expressions. After changing `enc_d`, move the front-panel parts by the change in `enc_d/2` (−Y) and the IEC inlet and LM2596 by +Δ`enc_d/2`; after changing `enc_h`, check `ctl_z`, `iec_z` and `sw_z`. Their **cut-outs** do follow the parameters (`ctl_x`, `ctl_z`, `sw_x`, `iec_x`, `iec_z`, `ban_z`).
- Panel heights (`ctl_z` 55, `iec_z` 52, `ban_z` 14, `split_z` 23) are measured from the floor and are not scaled with `enc_h`.
- Check clearances after a change: a smaller `enc_d` brings the floor vents, feet and clips closer to the standoffs and keep-outs. Below about 105 mm wide the rocker cut-out (`sw_x` 44.5) and the controller cut-out (`ctl_x` −9, 81.6 wide) reach the side walls, so move `sw_x` and `ctl_x` first. `inspect.parameter_sweep` rebuilds a copy of the design for a list of values and reports failures; a full rebuild takes about 90 s.

---

## 8. Open items

| # | Item | Status |
|---|---|---|
| 1 | Rocker switch: modelled from the KCD1-101 datasheet (cut-out 19.2 × 13, body 13.2 deep, 7.5 mm tabs). Flange thickness (2), rocker width (11) and clips are estimates; widen the hole 0.1–0.2 mm if a test print is tight | ✅ |
| 2 | Schurter snap tabs sit 1.4–3.4 mm behind the flange; check that they lock on a 2.5 mm wall | ⏳ |
| 3 | Banana sockets: own model (`Banana_4mm_*.sc`, 2026-11-05) with the two plastic pieces either side of the 2.5 mm wall, origin on the outer face (Y −75); no overlap with the wall, no import warnings. Nozzle measured Ø7.5, so the panel hole is Ø8 (`ban_hole_d`, 2026-11-07); the metal reaches 14 mm inside (Y −58.5), 0.4 mm short of the EMI filter box on the PSU (green socket) | ✅ |
| 4 | Confirm the bulk capacitor is no taller than 27 mm (0.9 mm gap to the controller) | ⏳ |
| 5 | Print the clip test box (`clipTest.sc`, §2.3a); tune the hook and arm for PETG or ASA | ⏳ |
| 5a | Print the insert test (`insertTest.sc`, §2.3b); set `psu_boss_hole` / `lm_boss_hole` to the hole that holds best: Ø4.2 (2026-11-08) | ✅ |
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
| 2026-11-01 | Measured rocker is larger (15 × 21 flange): new `Rocker_Switch_15x21.sc`; width 110 → 120 (`PSU_Enclosure_120x85.sc`); controller and bananas X −2, switch X 44.5, side clips, lip and groove moved out 5 mm |
| 2026-11-01 | IEC cut-out 48.1 × 28.1. Parametric rework (v3.1): split on a construction plane at `split_z`; lip and groove sketches dimensioned; bosses replaced by expression-placed standoffs; vents, feet, clips, hooks and pockets derived from `enc_w`, `enc_d`, `split_z`, `wall` and the fan (§7.2). Geometry unchanged at the defaults. Pre-rework file is in git history (commit 9850312) |
| 2026-11-01 | Lip and groove rebuilt from two splits and two trims (§2.1) after the lip union failed at widths ≤ 110 and depth 135. Rebuilds verified at W 100–140, D 120–180, H 70–110, split 20–28, wall 2–3, corner 4–7 |
| 2026-11-01 | LM2596 posts made square with a 45° gusset (printable lid-down without support). Name "cREATRON DPS XY-SK60X" recessed 0.3 mm into the lid, 10 mm from the front, 71 % of the width |
| 2026-11-01 | Red and green sockets swapped (black, green, red). NEG / EARTH / POS labels above the seam over the sockets and MAINS above the rocker, recessed 0.3 mm into the front of the top half |
| 2026-11-01 | Socket row centred on the box (`ban_x` 0) at 25 mm pitch (was 19 mm about the display centre), so the labels read clearly |
| 2026-11-02 | Rocker switch from the KCD1-101 datasheet (`Rocker_Switch_KCD1-101.sc`); cut-out 19.2 × 13 (was 12.75 × 18.45 measured) |
| 2026-11-02 | Lip and seam built from a copy and oversize box cuts instead of two splits and two joins (§2.1): the Split1/Split2 "Boolean retry" warnings are gone, seam exactly at Z 23. Rebuilds verified at W 100–140, D 120–180, H 70–110, split 20–28 |
| 2026-11-02 | Front labels (NEG / EARTH / POS / MAINS) scaled to 80 %: new `label_h` = `name_h * 0.8` (3.76 mm); the lid name keeps `name_h` |
| 2026-11-02 | Banana socket models moved 2.5 mm back (Y −72.2) to match the real parts; wall overlap in the model accepted |
| 2026-11-05 | Clip test box `clipTest.sc` (40 × 50 × 28, split Z 13) with the main design's lip, seam and 6 clips, plus its two 3MF halves |
| 2026-11-05 | Own banana socket model `Banana_4mm_*.sc` replaces the vendor STEP (open metal shell): front cap in front of the panel, Ø6 nozzle through the Ø6 hole, rear piece behind; the design now rebuilds without any warnings |
| 2026-11-07 | Project moved to `DPS_XY-SK60X/`. Vendor STEP sources in `stepFiles/`; unused models removed (vendor-STEP banana sockets, `oldTry/`, layout v2, 110 × 85, pre-parametric copy; all in git history). Two early designs kept in `backup/` |
| 2026-11-07 | Banana sockets measured: nozzle Ø7.5 (was Ø6), metal 14 mm behind the panel inner face (new `in_len`, was 10). Rear piece bore Ø7.5, panel holes `ban_hole_d` 6 → 8 mm; `Enclosure_Bottom.3mf` re-exported |
| 2026-11-07 | PSU turned 180° (AC terminal now at the rear right under the IEC inlet, DC terminal at the front behind the bananas) and moved 13 mm back (`psu_y` −5.1 → 7.9; the board's rear edge is 7.2 mm from the inner rear wall). Standoffs Ø9 (was 8) with Ø4 holes (was 3.5) for M3 heat-set inserts Ø5 × 4. Closest gaps: EMI filter 2.2 mm to the LM2596 capacitor, secondary heatsink 3.4 mm to the XY-SK60 capacitors, primary heatsink 3.8 mm to the IEC inlet |
| 2026-11-07 | `AC-DC2416.sc`: the DC wiring keep-out in front of the DC terminal has its own length `dc_wire_clear` = 12 mm (was `wire_clear` 20, still used for the AC side). It now ends at Y −61.5 and still overlaps the green socket's metal tip (Y −58.5) by 3 mm; the real parts are 9 mm apart. All component links now point to files in the project folder |
| 2026-11-07 | LM2596 posts for the same M3 heat-set inserts as the PSU: 9 × 9 (was 6 × 6), Ø4 × 5 deep hole (was Ø2.5 self-tapping); `Enclosure_Top.3mf` re-exported |
| 2026-11-07 | 1 mm lead-in chamfers on the six insert holes (`insert_ch`). Fan screw holes countersunk Ø6.8 × 90° on the lid for M3 countersunk screws (`fan_csk_d`). Fan grille slots now end inside the fan circle (`fan_grille_r` 22): the outer slots are shorter, at least 3.3 mm from the countersinks |
| 2026-11-08 | Insert test `insertTest.sc` / `insertTest.3mf`: four Ø9 × 5 standoffs with Ø3.9–4.2 holes and 1 mm chamfers, labelled |
| 2026-11-08 | Insert test printed: Ø4.2 holds the inserts best. `psu_boss_hole` and `lm_boss_hole` 4 → 4.2 (the 1 mm chamfers follow); both 3MFs re-exported |
