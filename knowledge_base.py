"""
IPC-A-610 Standard & SMT Root-Cause Knowledge Base for PCB Manufacturing.
Grounds the SLM with engineering-grade standards and containment protocols.
Supports all 6 defect classes:
0: mouse_bite
1: spur
2: missing_hole
3: short
4: open_circuit
5: spurious_copper
"""

PCB_DEFECT_KB = {
    "missing_hole": {
        "full_name": "Missing Drill Hole / Via",
        "station_of_origin": "Mechanical Drilling / CNC Plating Station",
        "ipc_class_verdict": {
            "Class 1 (General)": "REJECT - Functional Failure (Component cannot mount)",
            "Class 2 (Dedicated)": "REJECT - Non-conforming to drill file coordinates",
            "Class 3 (High Reliability)": "CRITICAL REJECT - Complete board scrap"
        },
        "probable_root_causes": [
            "Broken micro-drill bit during CNC cycle without automated tool detection",
            "Drill file (NC drill) coordinates offset or missing layer instruction",
            "Plating through-hole (PTH) barrel blockage by dry film residue before copper deposition"
        ],
        "containment_action": "Halt CNC drill line D-04 immediately. Inspect drill spindle runout and verify tool breakage sensors.",
        "capa_preventive_action": "Implement automatic optical tool-breakage detection after every 500 hits."
    },
    "mouse_bite": {
        "full_name": "Mouse Bite (Conductor Edge Nick / Erosion)",
        "station_of_origin": "Chemical Etching / Routing & Breakaway Station",
        "ipc_class_verdict": {
            "Class 1 (General)": "ACCEPTABLE if conductor reduction is < 30%",
            "Class 2 (Dedicated)": "DEFECT if conductor width reduction exceeds 20%",
            "Class 3 (High Reliability)": "REJECT if conductor width reduction exceeds 10%"
        },
        "probable_root_causes": [
            "Localized photoresist chipping or poor UV exposure adherence along trace boundary",
            "Acid etcher nozzle pressure fluctuation creating turbulent over-etch spots",
            "Excessive mechanical breakout stress during panel singulation / depaneling"
        ],
        "containment_action": "Quarantine current panel rack. Measure remaining trace width with optical micrometer against 20% limit.",
        "capa_preventive_action": "Calibrate etcher conveyor speed and check etching bath ferric chloride concentration."
    },
    "open_circuit": {
        "full_name": "Open Circuit (Broken Trace / Discontinuity)",
        "station_of_origin": "Photolithography / Chemical Etching Station",
        "ipc_class_verdict": {
            "Class 1 (General)": "CRITICAL REJECT - Electrical Discontinuity",
            "Class 2 (Dedicated)": "CRITICAL REJECT - Functional Failure",
            "Class 3 (High Reliability)": "CRITICAL REJECT - Immediate Scrap"
        },
        "probable_root_causes": [
            "Foreign dust / particulate on glass phototool blocking UV polymerization of dry film",
            "Physical scratch on copper foil during automated pick-and-place conveyance",
            "Chemical over-etching due to prolonged immersion or stalled conveyor"
        ],
        "containment_action": "Trigger automated flying-probe continuity tester. Segregate panel batch #BP-209 for scrap logging.",
        "capa_preventive_action": "Clean phototool exposure glass in Class 10,000 cleanroom; inspect roller conveyor belts for burrs."
    },
    "short": {
        "full_name": "Short Circuit / Solder Bridge",
        "station_of_origin": "Etching Station / Solder Paste Printing (SMT)",
        "ipc_class_verdict": {
            "Class 1 (General)": "CRITICAL REJECT - Severe Electrical Hazard",
            "Class 2 (Dedicated)": "CRITICAL REJECT - Risk of thermal runaway / burnout",
            "Class 3 (High Reliability)": "CRITICAL REJECT - High-reliability violation"
        },
        "probable_root_causes": [
            "Incomplete chemical etching leaving unetched copper webbing between adjacent traces",
            "Solder paste slump or excessive squeegee pressure during stencil printing",
            "Insufficient solder mask dam thickness between closely spaced IC pads (< 0.1mm)"
        ],
        "containment_action": "Isolate board immediately to avoid power-on testing damage. Check if bridge is surface solder (reworkable) or copper (scrap).",
        "capa_preventive_action": "Wipe stencil bottom side every 3 print cycles; verify etch resist developer bath pH levels."
    },
    "spur": {
        "full_name": "Conductor Spur (Trace Protrusion / Burred Edge)",
        "station_of_origin": "Photolithography (Exposure) / Chemical Etch Line",
        "ipc_class_verdict": {
            "Class 1 (General)": "ACCEPTABLE if minimum electrical clearance (>= 0.1mm) is maintained",
            "Class 2 (Dedicated)": "DEFECT if spur reduces spacing between conductors below 75% of nominal rule",
            "Class 3 (High Reliability)": "CRITICAL REJECT - Conductor spacing violation; high risk of electrical arcing"
        },
        "probable_root_causes": [
            "Pin-hole light leakage or optical flare during UV exposure on the dry film photoresist",
            "Scratched photomask / direct imaging glass permitting unwanted copper exposure",
            "Uneven spray pressure from chemical etcher oscillating manifold causing incomplete localized etch"
        ],
        "containment_action": "Quarantine affected lot immediately. Measure residual clearance distance between spur tip and neighboring trace.",
        "capa_preventive_action": "Replace phototool film; inspect laser direct imaging (LDI) optics and de-clog chemical spray oscillating nozzles."
    },
    "spurious_copper": {
        "full_name": "Spurious Copper (Residual / Isolated Copper Island)",
        "station_of_origin": "Chemical Etch & Strip Station / Pre-lamination Wash",
        "ipc_class_verdict": {
            "Class 1 (General)": "ACCEPTABLE only if completely isolated and clearance to active traces is > 0.15mm",
            "Class 2 (Dedicated)": "DEFECT if isolated copper island violates design clearance or is unanchored",
            "Class 3 (High Reliability)": "CRITICAL REJECT - Risk of copper flake detachment causing intermittent short during vibration"
        },
        "probable_root_causes": [
            "Incomplete dry film resist stripping leaving localized protective mask during etching cycle",
            "Exhausted etching bath chemistry (low specific gravity / high copper saturation)",
            "Floating resist skin or copper flakes re-depositing on board surface in rinse cascade"
        ],
        "containment_action": "Halt panel infeed. Check board wash tank filters and measure copper island adhesion using tape test.",
        "capa_preventive_action": "Upgrade stripping tank recirculating filtration to 5-micron filter; automate chemical replenishment dosing."
    }
}