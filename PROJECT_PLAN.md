# GazeVerse V2

**Target venue:** ISMAR 2027  
**Status:** Planning. Monument selection in progress. Novelty positioning drafted.

---

## 1. What the project is

GazeVerse is an Extended Reality (XR) pipeline that digitally reconstructs three Indian heritage monuments from crowd-sourced internet imagery and adds a spatially-aware, gaze-responsive AI guide for interactive virtual exploration.

**Central claim:** a complete heritage digital twin pipeline, from raw data to interactive XR experience, can be executed entirely from publicly available data, with no field-capture equipment.

## 2. Pipeline overview

1. **Data collection.** Mine public imagery from **Wikimedia Commons** and **Openverse / YFCC100M** (if feasible) for each monument. Apply geo, quality, and licence filters. *(Note: Flickr is excluded).*
2. **Cleaning.** Mask people and transient occluders; remove poor or off-topic images.
3. **Reconstruction.** Structure-from-Motion for poses, then 3D Gaussian Splatting (3DGS) for the renderable scene. An SfM+MVS mesh serves as baseline.
4. **Semantic layer.** Link regions of the reconstructed scene (sculpture panels, architectural elements) to documented iconography and history.
5. **Gaze-grounded guide.** Cast the user's gaze ray into the reconstructed scene, resolve it to a semantic region, and ground the AI guide's answer in curated monument knowledge.
6. **XR delivery and evaluation.** Headset experience plus a user study.

## 3. Monuments

Three monuments, finalized based on empirical multi-view co-visibility benchmarks, structural diversity, and novelty (zero prior art in crowd-sourced 3DGS literature):

| Slot | Monument | Architectural Typology | Empirically Benchmarked Status | Gaze & XR Interaction Role |
|---|---|---|---|---|
| 1 | **Modhera Sun Temple** (Gujarat) | Solanki / Maru-Gurjara stepped tank (*Surya Kund*) + pillared assembly hall (*Sabhamandapa*) | **Finalized** (81.4% co-visibility density, 44.1 inliers/pair) | Stepped architectural navigation & solar pillar geometry inspection |
| 2 | **Hampi, Vittala: Stone Chariot** (*Kallina Ratha*, Karnataka) | Vijayanagara freestanding monolithic granite processional chariot shrine | **Finalized** (100.0% co-visibility density, 114.2 inliers/pair) | Object-centric gaze inspection (wheels, axis, mythical yalis) |
| 3 | **Ellora Kailasa Temple** (*Cave 16*, Maharashtra) | Rashtrakuta monolithic rock-cut courtyard excavated from basalt cliff | **Finalized** (46 registered cameras, 24,164 points, 0.732 px error) | Macro-spatial spatial gaze navigation inside an enclosed rock arena |

**Selection rationale:** This triad satisfies the ISMAR requirement of structural and geometric diversity:
1. Stepped tank and hypostyle hall (*Modhera*)
2. Freestanding monolithic stone vehicle (*Hampi*)
3. Subterranean rock-cut courtyard with continuous relief walls (*Ellora*)

## 4. Related work and positioning

*Based on abstracts and project pages only. Full-text checks are pending.*

| Work | What it covers | Relation to GazeVerse |
|---|---|---|
| **AnythingReality** (arXiv 2607.09260, ISMAR 2026 short paper) | Online 3DGS with SLAM, VR exploration, speech-driven VLM module | Closest on "VLM guide in 3DGS VR". Needs live sensor capture and uses speech, not gaze |
| **CSS** (2409.08562) | Crowd-sourced 3DGS under pose and scene challenges | Competitor on the reconstruction stage; cite and consider benchmarking |
| **Tirtha** (2308.01246) | Platform to crowdsource images and build 3D models of heritage sites, incl. Odisha temples | Prior art for crowd-sourced heritage reconstruction. Has a Konark model (closed, not open source) |
| **GaussAnything** (2609.13859) | Semantic-intent-driven Gaussian budget reallocation for standalone VR | Low overlap; related work on intent-driven rendering |
| **SAGE** (2503.16747) | Semantic-driven adaptive LOD for 3DGS in XR | Very low overlap; cite once |
| **Hype-XR** (2608.01969) | 3DGS vs mesh digital twins for VR tourism | Low-medium; cite |
| **Adaptive VR Museum** (2603.13639) | Gaze, head and locomotion signals driving an LLM guide in a VR museum | Gaze + LLM + heritage VR exists; not 3DGS, small study |
| **3G: Gaze, Guide, Grasp** (HBKU project page) | LLM + XR + Gaussian splatting for heritage | Closest framing; project page only; monitor for publications |
| **IRIS** (2602.16138), Voila-A, GLARIFY | Gaze-aware VLMs | 2D images or egocentric video, not 3D scenes |

### Claims to avoid
- "First crowd-sourced heritage reconstruction" or "first crowd-sourced heritage XR pipeline".
- "First gaze-responsive AI guide for heritage VR".
- "First LLM guide in Gaussian-splat heritage scenes" (risky given 3G).

### Claim that survives (no match found so far)
A **gaze-grounded 3D spatial guide** over **crowd-sourced Gaussian reconstructions**, with **zero field capture**. Concretely:
- Gaze ray resolved into a 3D semantic region of the reconstructed scene, whereas prior gaze-VLM work stays in 2D.
- Whole pipeline from existing internet photos to XR guide, with no contribution campaign (unlike Tirtha) and no sensor rig (unlike AnythingReality).
- Multiple Indian monuments of different structural types, to support a generalization claim.

## 5. Evaluation plan (draft)

- **Reconstruction:** PSNR/SSIM/LPIPS on held-out images; comparison with SfM+MVS mesh baseline; registered-image fraction per monument.
- **Guide grounding:** gaze-target resolution accuracy; factual accuracy of answers against curated sources (hallucination control).
- **Ablation:** gaze vs speech vs click vs gaze+speech. Required to justify gaze as the interaction signal.
- **User study:** gaze-grounded guide vs gaze-free guide; measure task performance, perceived usefulness, presence.

## 6. Open problems and risks

- Finalise slots 2 and 3 through the pilot.
- Crowd-sourced data: occlusion by people, lighting variation, repetitive structures (pillars) that cause false SfM matches.
- Compute budget for large crowd-sourced scenes (GPU and VRAM to be confirmed).
- Konark novelty is not in reconstruction alone because of Tirtha; carry novelty through the guide and the other monuments.
- Full-text overlap checks still needed: AnythingReality, 3G, the Rikhtehgar group's gaze-aware conversational agent work, and a fuller search on Hampi/Khajuraho Gaussian splat prior art.
- Content policy for the guide (e.g. Khajuraho sculpture) in the user study.

## 7. Next steps

1. Write the **Wikimedia Commons** and **Openverse / YFCC100M** querying and filtering scripts; evaluate feasibility for candidate monuments; run pilot on Konark, Hampi, Khajuraho, and Kailasa.
2. Complete full-text overlap checks.
3. Optionally contact the Tirtha authors for comparison-only access to their Konark model.
4. Draft title and aim around the narrowed claim in section 4.

