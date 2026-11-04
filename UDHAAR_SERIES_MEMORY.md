# UDHAAR: 47 Names — Series Memory & Production Bible (Claude continuity file)

> **For Claude, at the start of any new chat:** read this whole file before doing anything. It records every decision already made for the series, the exact look and sound, the production pipeline, and what has been published. Then ask the person for (1) the story bible .docx, (2) the latest `UDHAAR_project.zip`, and (3) the **real vote result** of the last posted episode, if any. Never guess a vote result. Never break the rules in section 2.

> **For the creator:** in every new chat, attach three things: this file, the story bible (`UDHAAR_Story_Bible.docx`) and the latest project zip. Then say which episode to make and give the real winning vote, its winning percentage and the top comment from the previous episode.

---

## 1. Series at a glance

- **Format:** Instagram Reels, vertical 9:16, 1080×1920, 30 fps, about 60–90 s each (the pilot ran 92 s).
- **Language:** Roman Hindi narration and captions. Synthesis reads from Devanagari internally.
- **Narrator:** **Kabir Verma only.** He is 26 and soft, intimate, restrained and conversational. Every other character's words are reported by Kabir ("Kehne lage ki…"). No other voices, ever.
- **Structure:** Pilot (Day 0) → Episodes 1–47 (Day 1–47) → Day 48 epilogue (one of six endings).
- **Votes:** Episodes 1–46 end with a vote. Forty of them are ASK / LET GO, and six are story votes (Eps 7, 15, 20, 33, 40, 44). Each vote decides what happened after that episode, and the outcome is narrated at the start of the next episode. The pilot has no vote.
- **Status bar on every frame of Eps 1–47:** `DIN N/47 | WE OWE ₹… | COLLECTED ₹… | LET GO …`. Show only real, verified values.

## 2. Non-negotiable rules (from the bible plus our own decisions)

1. One voice: Kabir. Never write dialogue in other voices.
2. Show only facts from the current episode. Never anticipate later reveals: Route 47, Papa as the driver, Meera, the adoption, Bhatia's guilt, and so on.
3. Never invent vote results, percentages, comments or money. Ask the creator for them.
4. The **red cloth ledger is the only saturated red** in the images. All other reds are muted. Overlay text stays cream; the only red overlay element is the small underline on the series tag.
5. Each image lasts 2.0–3.0 s, and cuts follow the meaning of the words. Allowed transitions: hard cuts with a 0.12 s dissolve, and slow camera drift or zoom (1.00 ↔ 1.06–1.10). No morphing, no lip-sync, no talking heads.
6. Images contain no AI-generated text. All readable words are clean overlays or deliberate handwriting set in the Kalam font.
7. Burnt or destroyed props never reappear. Track the ledger, the bell and the trunk across branches (see the bible's continuity locks).
8. Be honest about tool limits. Never claim an unrendered video is finished.

## 3. Look: art direction (locked in the pilot)

**Style:** painted-paper graphic novel. The look comes from cut-paper **contre-jour silhouettes** with warm rim light, layered fog planes, ink-wash gradients, paper texture, pigment granulation and fine film grain. It is muted and overcast, with warm tungsten interiors. Faces are mostly in **profile**: either a dark silhouette with a rim, or a warm, side-lit profile. Close-ups of objects carry much of the story.

**Pipeline:** shot-specific Python writes the SVG → Chromium (Playwright) renders it at 1188×2112 (1.1× for drift room) → `post.py` applies the painterly finish → the editor crops to 1080×1920 with motion.

**Grades** (`post.py`):
- `dawn`: funeral and exteriors
- `day`
- `tungsten`: night interiors
- `night`
- `memory`: sepia flashbacks
- `neutral`: the end card

The `protect_red` setting keeps the ledger saturated.

**What failed, so don't do it again:**
- The stroke-based "painter" pass produced Van Gogh swirls and fuzz. Don't use it.
- Top-down crowds turned figures into pawns or pins.
- Mid-grey figures with dark face ovals looked uncanny. Use full silhouettes against bright haze instead.
- A dark face inside a hood read as a void. Expose the face edge against light, or side-light it.
- Capsule-segment hands read as gloves. Use the traced hand outlines (`HAND_R5`, `HAND_L3`).
- Bald mannequin heads on large profiles. Always add hair and keep necks thin.
- Pyres or biers drawn as flat white boxes read as cakes.
- Negative-scale transforms combined with SVG filters produced grey, semi-transparent figures. Use `manq.flipP()` instead.
- Radial-gradient ellipses left hard visible edges. Blur them (`b40`).

### Palette anchors
| Element | Colour |
|---|---|
| Dawn sky | `#5d6a73` → `#e3cfa9` → warm haze `#efdcb8` |
| Rim light | `#f7dcab` / `#f8ddaa` |
| Silhouettes | `#2c2b29` |
| Verma interior wall | distemper green `#4e5a51` / `#58645c` |
| Floor | grey mosaic `#5c5a53` |
| Tungsten bulb glow | `#ffe2a6` → `#f3b45e` |
| Kabir's faded blue shirt | `#6f8aa0` (dark `#4f6678`) |
| White kurta (funeral) | in shadow `#4a4945`–`#8c887d` |
| Papa's khaki uniform | `#a08a62` / `#7a6646` |
| Red ledger | `#c8202a` → `#a5141e` → `#6e0c14`, woven cloth texture |
| Brass bell | gradient `#e9c56a` → `#5a4016` |
| Ledger paper | `#efe5cc` → `#d8c8a6`, blue rules `#9fb2b6`, red margin `#d08a8a` |
| Papa's ink | `#1f2142` / `#26284a`, Kalam font |

### Characters (locked designs, defined in `scripts/shapes.py`, `manq.py`, `papa_face.py`)
- **Kabir Verma (26):** `KABIR_PROFILE` and `KABIR_HAIR` (short, slightly tousled), light stubble, thin neck. He wears a **white kurta at the funeral** and a **faded blue shirt from the notice onward**. `kabir_lit()` is his warm, side-lit profile and `kabir_kurta()` his torso. Seen from behind: a dark round head with short hair.
- **Ma / Sudha (54):** `MA_L` profile, mirrored when facing right, with a soft chin. A **white widow's saree with the pallu over her head**, no bindi. She is a tailor with a black sewing machine (s15). Her face is warm and side-lit, her eyes lowered. She is restrained and afraid. She knows more than she says.
- **Papa / Mohan Lal Verma** (died at 59; municipal bus driver for 31 years): a sepia studio portrait (`papa_face.py`). Khaki uniform with epaulettes, a full Indian moustache, short oiled hair greying at the temples, kind heavy-lidded eyes. On the wall the portrait has a marigold garland, a chandan tilak on the glass and a diya below it. For the 2001 flashbacks, draw the same face in his mid-thirties.
- **Shankar (70):** Platform 4 tea seller. Thin and stooped, with a walking stick, a grey wool shawl over his kurta, white hair at the sides and white stubble. **Three fingers on his LEFT hand** (ring and little finger missing, healed stumps; `HAND_L3`). His prop is a chipped-edge chai glass. At the funeral he cried at Papa's feet.
- **Mourners:** silhouette types `man`, `manc` (hands clasped), `woman`, `womanc`, `boy` (`shapes.SHAPES`). The jointed mannequin poses live in `manq.py`: `old_walk`, `old_kneel`, `sit_floor`, `stand_front`, `stand_side`, `sew`.

### Locked props and places
- **Red cloth ledger:** cloth-bound with a string tie, **one name per page**. The first page carries only Papa's line "किसी से पैसे मत माँगना।" Each name page shows the name, the amount and the year in Papa's handwriting (Kalam). The **last page (#47)** is scratched out until the paper tore. The ink is near-black with a hint of very dark red, a subtle plant for the red pen in Ep 3–4.
- **Brass bus bell** (`art.bell()`): a dome bell with a top knob and a clapper. Kabir was never allowed to touch it. The "47" engraved inside **must not be shown until Ep 8**.
- **Tin trunk:** blue-green painted tin with rust and brass hasp, kept under the iron cot. Inside are the folded khaki uniform, the bell and the ledger at the bottom.
- **Verma house:**
  - a small plastered house in a narrow Ranipur lane, with overhead wires and a streetlight
  - blue-green double wooden door with an iron hasp and padlock, and a faded rangoli at the threshold
  - inside: a single hanging bulb, distemper-green walls, a grey mosaic floor and an iron cot
- **Papa's things:** worn rubber chappals with faded blue straps, reading glasses, and a steel tumbler.
- **Bank notice:** white printed paper with tape corners, pasted on the door.
- **Municipal bus:** muted blue-grey with cream windows. It has appeared once, distant, at the end of the pilot.

### Text and overlay design (`edit/render.py`)
- **Captions:**
  - Mukta Bold 58 px, cream `(250,240,222)` with a thin dark stroke and a soft dark rounded backing.
  - Centred at y ≈ 1335, or moved lower when a frame's key graphic sits there.
  - Chunks of 6 words or fewer, breaking at punctuation, with karaoke-style word reveal (upcoming words at about 47% opacity).
  - Safe zone: x 90–990, y 250–1600.
- **Series tag** (top left, first ~4 s): `UDHAAR · DIN N / 47` in Mukta SemiBold 30 with a thin red underline. From Ep 1 on, it is replaced by the status bar.
- **Big numbers:** Mukta ExtraBold in cream. Counters in Rozha One. Handwritten amounts on paper in Kalam Bold, blue-black.
- **End card:** red cloth texture with:
  - "उधार" in Rozha One 250
  - "U D H A A R · 4 7 N A M E S"
  - "EPISODE N · KAL" in warm cream
  - a one-line teaser and call to action
- **Fonts:** Kalam, Mukta, Rozha One, Tiro Devanagari Hindi, Hind, Martel, Yatra One, Caveat, all from Google Fonts, in `fonts/`.

## 4. Sound: voice, music, mix

- **Voice engine:** Supertonic 3 multilingual (sherpa-onnx v1.13.8 CLI), **speaker id 8** (the "M4" style: soft, youthful male), `--lang=hi --num-steps=24`, line speed 0.95–1.00. It reads Devanagari text. Checks showed native-sounding Hindustani: in Whisper's language detection the leftover probability went to Urdu, not English.
- **Process:**
  1. Record 4 takes per line (`scripts/gen_takes.sh`).
  2. Score every take with a forced-alignment check (`scripts/score_fast.py`, `score.py`; numpy Whisper-turbo in `scripts/asr.py`).
  3. Keep the best take, then confirm it by transcription.
  4. Apply `atempo=1.06` to all takes.
  5. Multiply the pauses between lines by 0.7.
  6. Gate the silences, which removes a faint 1.2 kHz vocoder hum.
  7. Run `scripts/build_vo.py`, which writes `edit/vo.wav` and `vo_lines.json` (line times plus internal segments for the captions).
- **Known pronunciation fixes:**
  - "काग़ज़ ही" came out as "kaagzar", so spell it "कागज ही".
  - "अड़तीस लाख दे गया" came out as "laag de", so the line was rephrased to "लाख बाँट गया".
  - **"lakh" before a consonant: spell it "लाख़"** (with the nuqta). In Ep 1, "इक्कीस लाख़ के आगे" was the only spelling that came out clean.
  - Use "ग्लास" for "glass", so it is spoken as captioned rather than as "gilaas".
  - Always check transcripts for nuqta (dotted-consonant) and final-"kh" problems. Write numbers as words.
- **Model downloads** (GitHub release assets are reachable from the workspace; Hugging Face and PyPI are not):
  - `https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.8/sherpa-onnx-v1.13.8-linux-x64-shared.tar.bz2`
  - `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2`
  - `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2`
  - Fonts: sparse `git clone` of `github.com/google/fonts` (`ofl/kalam`, `ofl/mukta`, `ofl/rozhaone`, …).
- **Score and sound effects:** everything is synthesized in `sound/synth.py`, `sound/score.py` and `sound/mix.py`. There are no licensed samples.
  - **Score:** centre key D, a sparse felt-piano motif (Bb3 A3 Eb4 D4, Bhairav/Todi colour), a tanpura-like drone, a soft heartbeat pulse, clock ticks for the countdown, and a restrained bowed swell for shocks. Music anchors: `drop_at`, `diary_reveal`, `torn_page`, `final_bell`.
  - **Signature:** a **brass bell "ding-ding"** at the very start and at the final line of every episode.
  - **Beds:** `dawn`, `night_room`, `morning_lane` (`bus_at`), `room_tone`.
  - **Sound effects:** `bell_dingding`, `bell_clink`, `trunk_open`, `latch`, `cloth`, `page_turn` (variants 0–3), `page_flutter`, `paper_handle`, `paper_tear`, `passbook_flip`, `notice_rustle`, `pencil`, `ma_arrives`, `footsteps`, `door_creak`, `breath`, `clock_tick`, `crackle`, `kite`, `dog_far`, `bus_pass`, `horn_far`, `whoosh`.
  - **Mix targets:** about -14 LUFS integrated, true peak -1 dBTP or lower, the voice dry and in front, music 24–37 LU under speech with ducking.
  - **Per-episode score:** put a `score_profile` value in the timeline (for example `"ep01"`), and `mix.py` then loads `sound/score_ep01.py`. Each episode gets its own small arrangement built from the same instruments and the series motif. The pilot uses the default `score.py`.
  - **Station sound:** use the `morning_lane` bed (with `bus_at` null) plus `horn_far`, `crackle` (kerosene stove) and `footsteps`. No announcements.
- **Export:** `ffmpeg -c:v libx264 -preset veryfast -crf 20 -maxrate 12M -bufsize 24M -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart`.

## 5. Writing voice (Kabir)

- Write natural, conversational Roman Hindi with conjunctions ("aur", "lekin", "toh", "phir", "jab") so sentences flow into each other.
- Use restrained suspense and specific physical details: chappals, a steel tumbler, a diya.
- Report other characters through Kabir: "boli ki diary waapas rakh do".
- **Avoid:**
  - the "X nahi tha. Y tha." contrast cliché
  - strings of dramatic one-liners
  - trailer-style lines and forced poetry
- Use at most one deliberate parallel line per episode, for example "Naam gine toh saintalis nikle. Aur bank ne kitne din diye the? Saintalis."
- **Shape of each episode:**
  1. a cold hook in the first 2 seconds
  2. the previous vote's outcome, told briefly by Kabir (Ep 2 onward)
  3. the day's encounter
  4. an emotional complication
  5. the dilemma
  6. the vote question
  7. the end card
- Aim for 150–190 spoken words, about 70–85 s of speech.

## 6. Published episodes log

### Episode 0 (Pilot) · Day 0 · "Forty-Six Strangers" — DONE (92.0 s)
File: `UDHAAR_Ep0_Pilot.mp4`. There was **no vote**. The end card says: "EPISODE 1 · KAL — Naam #1: Shankar. Maangu ya chhod doon? Faisla aapka hoga."

**Final narration (as spoken and captioned):**
1. Papa ke antim sanskaar mein chhiyaalis log aaye the, aur main unmein se ek ko bhi nahi jaanta tha.
2. Woh log bhi ek doosre ko nahi jaante the.
3. Lekin Ma ne kisi se kuch nahi poochha.
4. Phir ek buzurg aage aaye, Papa ke pairon ko haath lagaaya, aur wahin baith kar rone lage.
5. Baar baar bas yahi keh rahe the ki woh Papa ke paise kabhi lauta nahi paaye.
6. Papa ne ikatees saal bus chalaayi thi, aur unke bank khaate mein sirf do sau baarah rupaye the.
7. Pehli baar laga ki main apne Papa ko jaanta hi nahi tha.
8. Teen hafte baad bank ka notice aaya. Papa ne ghar girvi rakha tha, aur mujhe bataaya tak nahi.
9. Ikkis lakh chukaane the, saintalis din mein. Warna ghar chala jaayega.
10. Usi raat maine Papa ka puraana baksa khola.
11. Wardi ke neeche unki peetal ki ghanti thi, jise woh mujhe kabhi chhoone nahi dete the.
12. Aur sabse neeche, ek laal kapde ki diary.
13. Andar naam the, tareekhein thi, aur har naam ke aage ek rakam.
14. Maine jod kar dekha. Adtees lakh, chaalis hazaar.
15. Do sau baarah rupaye waala aadmi, adtees lakh baant gaya?
16. Naam gine toh saintalis nikle. Aur bank ne kitne din diye the? Saintalis.
17. Lekin pehle panne par Papa ne bas itna likha tha, ki kisi se paise mat maangna.
18. Aur aakhri naam ko kisi ne itni baar kaata tha ki kaagaz hi phat gaya tha.
19. Main wahi panna dekh raha tha jab Ma darwaaze par aa gayi, aur dheere se boli ki diary waapas rakh do.
20. Unki aawaaz kaanp rahi thi. Maine Ma ko itna dara hua kabhi nahi dekha tha.
21. Maine diary waapas nahi rakhi.
22. Pehla naam hai Shankar. Kal main unse milne jaa raha hoon.

**Shot list (seconds):**

| Time | Shot | Image |
|---|---|---|
| 0–3.3 | s01 | Backlit dawn cremation ground: mourners standing apart, pyre, peepal tree, smoke, Kabir's head in the foreground. The faint **wheelchair figure** (Kamakshi plant) is at the far left. |
| 3.3–5.7 | s02 | Kabir's rim-lit profile with the crowd blurred behind |
| 5.7–8.0 | s03 | Strangers scattered in fog, each alone |
| 8.0–10.2 | s04 | Ma in profile, white pallu, eyes lowered |
| 10.2–12.2 | s05 | Shankar walking in with his stick |
| 12.2–14.4 | s06 | **His hands on Papa's shrouded feet; the left hand has three fingers** |
| 14.4–16.9 | s07 | Shankar kneeling at the bier, Kabir watching |
| 16.9–19.4 | s08 | Kabir's reaction profile |
| 19.4–21.8 | s09 | Papa's garlanded portrait |
| 21.8–24.6 | s10 | Passbook with the "₹ 212.00" overlay, his reading glasses and tumbler |
| 24.6–26.7 | s11 | Papa's chappals in the foreground, Kabir in silhouette in the doorway |
| 26.7–28.7 | s11b | Kabir's face lit by the diya |
| 28.7–30.9 | s12 | The front door with the notice |
| 30.9–33.9 | s14 | The house at dusk, Ma at the window |
| 33.9–36.6 | s13 | Kabir's hands holding the notice ("₹ 21,00,000", then "47 दिन") |
| 36.6–38.9 | s15 | Ma at her sewing machine |
| 38.9–41.5 | s16 | The trunk opened, with Kabir's shadow on the wall |
| 41.5–43.9 | s17 | Uniform with the bell and a sliver of red |
| 43.9–46.3 | s18 | Memory: Papa's hand over the bell, a child's hand reaching for it |
| 46.3–49.0 | s19 | **The red ledger revealed** |
| 49.0–52.0 | s20 | Pages: तारा ₹40,000 2011 / दीपक-दिलीप ₹60,000 2012 |
| 52.0–55.0 | s21 | The total, ₹38,40,000, added up on the back of the notice |
| 55.0–57.9 | s22 | Passbook beside the ledger (pages for सलीम and गौरी) |
| 57.9–60.5 | s23 | Pages fanning, count overlay 1→47 |
| 60.5–63.2 | s24 | Clock and calendar ("47 दिन") |
| 63.2–65.9 | s25 | The first page: "किसी से पैसे मत माँगना।" |
| 65.9–68.2 | s26 | Close-up of the handwriting |
| 68.2–70.6 | s27 | Page 47, scratched out and torn |
| 70.6–72.8 | s28 | Light through the tear |
| 72.8–75.7 | s29 | Wide: Kabir on the floor with the ledger, Ma in the doorway |
| 75.7–78.4 | s30 | Ma's lit face |
| 78.4–80.4 | s31 | Ma's trembling hand on the door frame |
| 80.4–82.9 | s32 | Kabir looking up |
| 82.9–84.9 | s33 | The ledger held against his blue shirt |
| 84.9–86.9 | s34 | "1. शंकर" (the amount is blurred) |
| 86.9–89.4 | s35 | Dawn: Kabir walking down the lane, a bus at the far end |
| 89.4–92.0 | s36 | End card |

**Clues planted for rewatchers:**
- Shankar's three-fingered hand. The pilot never says he is Shankar; Ep 1 reveals it.
- A wheelchair figure at the funeral (Kamakshi; paid off in Ep 47).
- "Ma didn't ask anyone" and her fear.
- 46 mourners but 47 names.
- Papa mortgaged the house without telling Kabir.
- The bell Kabir was never allowed to touch.
- Strangers who don't know each other (paid off by the Ep 36 WhatsApp group).

**Small creative additions in the pilot that are not in the bible** (to be treated as canon from now on):
- Kabir didn't know about the mortgage.
- Papa never let Kabir touch the bell.
- Kabir added up the total on the back of the notice.
- The calendar shows ten days crossed.

### Episode 1 · Day 1 · #1 Shankar, tea seller · ₹6,000 (2003) — DONE (71.0 s)
File: `UDHAAR_Ep1_Shankar.mp4`. Vote shown: **ASK / LET GO** (the first counted vote). The status bar runs on every story frame: `DIN 1/47 | WE OWE ₹21,00,000 | COLLECTED ₹0 | LET GO 0`.

**Final narration:**
1. Papa ke antim sanskaar mein jo buzurg unke pairon par ro rahe the, kal tak woh mere liye bas ek ajnabi the.
2. Aaj pata chala, unka naam Shankar hai.
3. Diary mein unke naam ke neeche Papa ne bas itna likha tha, platform chaar.
4. Subah station pahuncha, toh platform ke aakhri kone mein ek chhoti si chai ki dukaan thi.
5. Mujhe dekhte hi woh ruk gaye, aur bole ki meri chaal bilkul Papa jaisi hai.
6. Phir chhappar ke neeche tange ek hook se ek puraana glass utaara. Kinaara toota hua tha.
7. Kehne lage ki Papa isi glass mein chai peete the, aur unhone use teis saal se sambhaal kar rakha hai.
8. Maine unke haath dekhe. Baayein haath mein sirf teen ungliyaan thi. Wahi haath, jo us din Papa ke pairon par the.
9. Mujhe samajh nahi aa raha tha ki koi ek bus driver ko itna kaise yaad rakh sakta hai.
10. Diary mein Shankar ji ke naam ke aage chhe hazaar rupaye likhe hain. Saal do hazaar teen.
11. Ikkis lakh ke aage chhe hazaar kuch bhi nahi, phir bhi ghar bachaane mein har rupaya kaam aayega.
12. Lekin jis aadmi ne Papa ka ek glass itne saal bacha kar rakha, usse main hisaab kaise maangoon?
13. Aap hote toh kya karte?

**Shot list (seconds):**

| Time | Shot | Image |
|---|---|---|
| 0–2.4 | e01 | Hook: Shankar's three-fingered hand around the chipped glass |
| 2.4–4.5 | e02 | Funeral memory: him bowed at the bier |
| 4.5–6.9 | e11 | Him behind the kettle steam |
| 6.9–9.2 | e07 | His side-lit profile, with the name tag "SHANKAR · Naam #1 · Platform 4 ki chai" |
| 9.2–11.9 | e03 | The ledger page "1. शंकर", amount blurred, Papa's note "प्लेटफ़ॉर्म चार" |
| 11.9–14.3 | e04 | Platform 4 wide, with the yellow "4" board |
| 14.3–16.6 | e05 | Kabir walking the platform |
| 16.6–18.9 | e06 | The stall with the hook glass |
| 18.9–21.0 | e08 | Two-shot at the stall |
| 21.0–23.4 | e10 | Memory: Papa in khaki and cap, walking the same platform |
| 23.4–26.0 | e12 | Hand lifting the glass off the hook |
| 26.0–28.7 | e13 | The chipped rim |
| 28.7–31.4 | e14 | Memory: Papa's hand around the same glass |
| 31.4–33.4 | e15 | The pour |
| 33.4–35.4 | e16 | Two glasses steaming |
| 35.4–38.6 | e17 | **The three-fingered hand on the counter** |
| 38.6–41.6 | e18 | Callback: the pilot's s06 hands-on-feet frame, in the memory grade |
| 41.6–44.0 | e19 | Kabir's lit profile |
| 44.0–46.7 | e20 | A faded municipal bus beyond the platform end (bible beat) |
| 46.7–49.6 | e21 | The page: ₹6,000, 2003 |
| 49.6–51.8 | e22 | Handwriting macro |
| 51.8–54.4 | e23 | Notice beside the glass, overlay "₹21,00,000 vs ₹6,000" |
| 54.4–57.0 | e24 | The house door with the notice, Ma's shadow at the window |
| 57.0–59.8 | e25 | The glass alone on its hook in a sunbeam |
| 59.8–62.6 | e26 | Two-shot silhouette |
| 62.6–65.0 | e27 | Kabir alone on the platform |
| 65.0–71.0 | e28 | Vote card |

**Vote card design** (`ep01/edit/render.py`, overlay `vote`), on red cloth:
- "DIN 1 KA FAISLA · AAPKA"
- The question: "Shankar ji se paise maangoon?"
- Two outlined buttons:
  - "ASK — Shankar ji se ₹6,000 maango"
  - "LET GO — Unka panna chhod do"
- "Comment karo: ASK ya LET GO"
- The rules line: "Ek account, ek vote. Vote band: Episode 2 se 2 ghante pehle." and "Tie hua toh Papa ka ek rupaye ka sikka faisla karega."
- "EPISODE 2 · KAL"

The bell ding-ding plays on the final line.

**New canon from Ep 1:**
- Papa's note on Shankar's page reads "प्लेटफ़ॉर्म चार".
- Shankar is bald, with white stubble, a short white moustache and a grey shawl.
- The chipped glass hangs alone on a hook under the tin awning.
- Papa walked the platform in his khaki uniform and cap (memory shot).
- Do **not** show Shankar's old biscuit box or any Route 47 ticket before Ep 2's ASK outcome.

**New assets:** `scripts/station.py`:
- `chai_glass()` (chipped)
- `kettle()`, `stove()`
- `canopy()`, `pillars()`, `number_board()`
- `shankar_lit()`

`scripts/build_ep.sh EPDIR shot '{post}'` builds a single shot for any episode.


### Episode 6 · Day 6 · #6 Rukhsana Begum, tailor · ₹30,000 (2006) · "बहत्तर हज़ार" — DONE (94.4 s)
File: `UDHAAR_Ep6_Rukhsana.mp4` (project folder `ep06/`). Opening = **Ep5 ASK** (cheque taken). Vote shown: **ASK / LET GO**.
Header (first 5 s, bible v3 meters): `DIN 6/47 | QARZ ₹21,00,000 | JAMA ₹1,71,000 | SAATH 1` + `KAL KA FAISLA: ASK` (no % supplied).
VO: the creator's own recording (`ep06/vo/vo_raw.wav`, 88.4 s, Supertonic voice), not re-synthesised. Captions are timed from it:
pause-split into 36 segments (`vo/seg.py`), each checked by Whisper (`vo/asr.txt`), words spread by syllables (`vo/make_lines.py`).

**Narration (Roman, as captioned):** Aapne kaha, cheque le lo. / Gauri ji ne ek lakh bees hazaar ka cheque diya, aur boli, "Hisaab barabar." /
Phir nazar pher kar bataaya, "Tumhare Papa ke aakhri shabd the... peetal ki ghanti... saintalis ko..." / Sunkar mujhe ghar mein rakhi Papa ki ghanti yaad aayi. /
Magar saintalis se unka kya matlab tha? / Diary ka saintalisvaan naam kata hua tha, aur ticket ka route bhi saintalis tha. / Unke aakhri shabdon mein mera naam nahi tha. /
Phir maine diary ka chhatha panna khola. / Usmein Rukhsana Begum ka pata tha, aur silaai machine ke tees hazaar rupaye likhe the. /
Unse milne Darzi Gali pahuncha, toh dukaan mein teen machinein chal rahi thi, jabki kone mein rakhi puraani kaali machine par koi nahi baitha tha. /
Maine unhe diary dikha kar machine ke paise lautaane ki baat ki, toh unka chehra utar gaya. / Boli, "Udhaar kis baat ka? Tumhare Papa baarah saal tak har mahine paanch sau dete the.
Kehte the, silaai ka advance hai, magar kabhi kuch silwaaya hi nahi. Ise udhaar kehna unki beizzati hai." / Maine hisaab joda, toh bahattar hazaar rupaye hue. /
Lekin diary mein sirf machine ke tees hazaar likhe the. / Har mahine diye gaye un paison ka kahin zikr nahi tha. / Agar Papa madad kar rahe the, toh kya machine ke paise bhi madad hi the? /
Rukhsana ji tees hazaar lauta sakti thi, lekin woh ise udhaar maanti hi nahi thi. / Doosri taraf, machine ka hisaab Papa ne diary mein khud likha tha. /
Unhone diary meri taraf sarka di. / Ab aap bataaiye, Papa ka likha maan kar paise maangoon, ya Rukhsana ji ki baat maan kar rehne doon?

**Shots** (`ep06/edit/edl.py`): c01 cheque torn off (Gauri's hands, white cuffs) · c02 cheque passed to Kabir (+₹1,20,000) · c03 Gauri profile at the window ·
c04 memory: Papa's hand on the hospital sheet (ID band) · c05 the bell in the dark + Kalam "पीतल की घंटी… सैंतालीस को…" · c06 open trunk, bell on the uniform ·
c07 Kabir under the bulb + "47?" · c08 page 47 scratched/torn, maroon pen · c09 Route 47 ticket, 47 circled · c10 Kabir eyes down over bell/page/ticket ·
c11 morning, diary opened · c12 page 6 (name, दर्ज़ी गली, ₹30,000 — मशीन, 2006) + reframe · c14 Darzi Gali over Kabir's shoulder · c15 three women at machines ·
c16 the old black machine, half under a cloth, empty stool · c17 cutting table: diary set down, her bangled hands · c18/c19 Rukhsana's face falls / chin up (name tag) ·
c20 memory: Papa backlit at the shop door with an envelope (₹500 · har mahine) · c21 envelopes in a tin (no stitched hems — held for Ep7) · c22 order book "मोहन लाल जी", empty ·
c23 Rukhsana, spectacles on · c24 the sum on the notice's back (12 साल × 12 = 144 महीने; 144 × ₹500 = ₹72,000) · c25 DIARY ₹30,000 vs LIFAAFE ₹72,000 ·
c26 finger down empty rows · c27 Kabir eyes down · c28 reframe of the old machine · c29 new cloth to the ceiling, machines busy · c30 Rukhsana looks away ·
c31 macro of Papa's "₹30,000 — मशीन" · c32 diary pushed back by her hand · c33 two-shot · c34 Kabir · vote card.
Vote card: "Papa ka likha maanoon, ya Rukhsana ji ki baat?" ASK — "Diary maano, machine ke ₹30,000 lo" · LET GO — "Unki baat maano, udhaar nahi tha".

**New canon / designs (Ep6):** Rukhsana (`ep06/people6.py rukhsana()`): late 50s, sage-green dupatta with gold border over her hair, mustard kameez,
measuring tape round the neck, spectacles on a cord (or on), green/gold glass bangles. Dr Gauri (`gauri()`): short black bob, white coat, stethoscope.
Shop: one yellow bulb, shelves of folded cloth, three treadle machines, the old black machine in the corner (half covered, nobody sits there).
Ticket face: "NAGAR BUS SEVA · ROUTE 47 · 9-1-2001 · ₹4". Papa's pen on page 47 is maroon (muted), not ledger red.
**New tools:** `ep06/hands6.py` — bone-built dorsal hands (poses FLAT, RELAXED, POINT, GRIP, PENCIL; sleeves, bangles, ID band, age). Use these for
every hand from now on instead of HAND_R5 outlines. `props6.py` (sewing machine, treadle table, cloth shelves, envelope, cheque, ticket, notice back,
order book, page47, worker silhouettes, Kabir back view). `ep06/build6.sh` builds shots (post limited to 3 parallel jobs — more runs out of memory).
Camera in `ep06/edit/render.py`: per-shot (zoom, focus) eased moves + overlays anchored to the still (circle, write-on sums, highlighter).
Sound: `sound/score_ep06.py`; `ep06/edit/mix6.py` adds `shop` (treadle machines; stop one by one on "chehra utar gaya", resume on "lauta sakti thi") and `hospital` beds.

### Episode 7 · Day 7 · #7 Bablu "Hero" · ₹50,000 (2007) · "पापा की आवाज़" — DONE (100.1 s)
File: `UDHAAR_Ep7_Bablu.mp4` (`ep07/`). Opening = **Ep6 ASK** (₹30,000 taken; "Ab main karzdaar nahi"). **Story vote: BATAO / CHHUPAO** (Ma ka sawaal).
Header (first 5 s): `DIN 7/47 | QARZ ₹21,00,000 | JAMA ₹2,01,000 | SAATH 1` + `KAL KA FAISLA: ASK`.
**On-screen text rule (creator, after Ep6): no floating labels, chips, name tags or comparison boxes. Only the bottom captions,
the 5 s header and the vote card. Any other readable text must be inside the picture (handwriting, the plate, the ticket, the calendar).**
VO: creator's recording `ep07/vo/vo_raw.wav` (93.9 s), 39 pause segments, Whisper-checked (`vo/asr.txt`).

**Narration (Roman, captioned):** Pichhle episode ke comments mein aapne kaha tha, "Machine ke paise le lo." Toh maine Rukhsana ji se tees hazaar rupaye le liye. /
Unke hisaab se Papa ne madad ki thi, isliye mera paise waapas maangna unhe bura laga. Paise mere haath mein rakhte hue boli, "Ab main karzdaar nahi." /
Wahaan se nikalne laga, toh unhone bataaya ki do hazaar ek ki sardi mein Ma ne Papa ke liye raat bhar kuch sila tha. / Raaste bhar main Papa se judi aisi baatein sochta raha,
jinke baare mein mujhe kuch pata hi nahi tha. / Ghar lauta, toh Gauri ji ke bataaye, unke aakhri shabd yaad aaye... "Peetal ki ghanti... saintalis ko..." /
Unka matlab samajhne ke liye bakse se Papa ki ghanti nikaali, aur saaf karne laga. Uske andar saintalis likha hua tha, wahi number jo ticket par tha. /
Tabhi Bablu Hero milne aaye. Diary mein unke naam pachaas hazaar rupaye likhe the, magar lautaane ke liye abhi paise nahi the, isliye maafi maangne aaye the. /
Baatein karte karte woh mohalle waalon ki nakalein utaarne lage, toh Ma bhi rasoi ke darwaaze par aakar sunne lagi. / Jaate jaate unhone Papa ke lehje mein kaha,
"Kabir... kisi se mat maangna." / Main thithak gaya, kyunki yahi baat diary ke pehle panne par likhi thi, jo unhone kabhi dekha hi nahi tha. /
Unke jaate hi Ma ne darwaaze ki kundi lagaayi aur poochha, "Aaj Rukhsana aayi thi. Tum Papa ki diary lekar logon se paise maang rahe ho?" /
Ma ko ab tak nahi bataaya tha ki ghar bachaane ke liye paise jama kar raha hoon. Sach bataata, toh woh mujhe rok sakti thi, lekin baat chhipaane ke liye unhi se jhooth bolna padta. /
Ab aap bataaiye, Ma ko poora sach bata doon, ya bas itna kahoon ki Papa ke doston se mil raha hoon?
Vote card: "Ma ko poora sach bata doon, ya bas itna kahoon?" BATAO — "Ma ko poora sach batao" · CHHUPAO — 'Bas itna: "Papa ke doston se mil raha hoon"'. Tie: heads = BATAO.

**Shots** (`ep07/edit/edl.py`): d01 her hand on ₹500 notes, cutting table · r_c16 the old machine · d02 notes pressed into Kabir's hand · r_c20 Papa's envelope (memory) ·
d03 Rukhsana turned away, hurt · d04 chin up "karzdaar nahi" · d05 Kabir leaving through the bright shop door · r_c30 Rukhsana telling · d06 memory 2001: young Ma
(muted indigo saree) sewing through the night by a lamp, frost on the window (the cloth is NOT identifiable) · d07 dusk lane over his shoulder · d08 Kabir thinking ·
d09 Verma door at dusk, notice taped · r_c04 Papa's hand on the hospital sheet · r_c05 the bell in the dark · d10 hands lift the dusty bell from the trunk · d11 polishing ·
d12 inside the dome: riveted brass plate engraved 47 · d13 ticket beside the plate · d14 Bablu at the door with a sweets box · d15 diary page 7 "बबलू 'हीरो' ₹50,000 2007" ·
d16 Bablu sheepish · d17 on the cot, palms joined · d18 cough impression (fist) · d19 cycle-bell impression · d20 Ma at the kitchen door, not smiling ·
d21 Bablu at the threshold, hand at throat · r_s09 Papa's portrait under "Kabir... kisi se mat maangna" · d22 Kabir stops dead · r_s25 first page ·
d23 empty threshold, sweets box left on the cot · d24 Ma's hand on the iron bolt · d25 Ma eyes lowered · d26 Ma looks straight at him · d27 the bell in his hands, diary behind ·
d28 the diary with notes tucked in + notice · d30 Ma's hand steady on the door frame · d31 Kabir eyes down · d32 wide: Ma at the door, Kabir on the cot, the bulb between · d33 Ma waiting.
(d29 Ma's calendar Dec 2026 with 11–17 crossed is built but not used.)

**New canon (Ep7):** the bell's "47" is a riveted brass plate inside the dome, engraved numerals (found this episode; Ep8 may refer to it, must not re-discover it).
Bablu (`ep07/people7.py bablu()`): 48, stocky, oiled pompadour that shines, thin moustache, muted mustard shirt with brown paisley print. Ma (`ma_lit()`) = pilot s30 construction.
Sweets box left behind on the cot. Ma bolted the door (iron kundi). Ma now knows Kabir is visiting people with the diary (Rukhsana told her, angry). Bablu's ₹50,000 never collected.
**Sound:** `sound/score_ep07.py` (music hard-muted from "Papa ke lehje mein kaha" to "kyunki..."), `ep07/edit/mix7.py` (+ `knock`, `bell_once`, `cycle_ting` SFX; shop bed in the opening).
**Renderer:** vote card text now comes from the EDL (`'vote'` overlay params: day, q lines, a/b labels+subs, tie, next).

## 7. Running state (update after every episode)

| Ep | Day | Vote shown | Real winner | % | Top comment | WE OWE | COLLECTED | LET GO |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | none | — | — | — | ₹21,00,000 | ₹0 | 0 |
| 1 | 1 | ASK / LET GO | ASK | — | — | ₹21,00,000 | ₹6,000 | 0 |
| 2 | 2 | ASK / LET GO | LET GO (watch returned) | — | — | ₹21,00,000 | ₹6,000 | 1 |
| 3 | 3 | ASK / LET GO | ASK | — | — | ₹21,00,000 | ₹31,000 | 1 |
| 4 | 4 | ASK / LET GO | ASK | — | — | ₹21,00,000 | ₹51,000 | 1 |
| 5 | 5 | ASK / LET GO | ASK (cheque taken) | not supplied | — | ₹21,00,000 | ₹1,71,000 | 1 |
| 6 | 6 | ASK / LET GO | ASK (₹30,000, in anger) | — | — | ₹21,00,000 | ₹2,01,000 | 1 |
| 7 | 7 | BATAO / CHHUPAO (story) | **pending: ask the creator** | | | ₹21,00,000 | ₹2,01,000 | 1 |

From Ep2 on the bible v3 meters are QARZ / JAMA / SAATH (JAMA = COLLECTED, SAATH = commitments of support). Ep6 header uses them.
**What Ep8 needs from the Ep7 result:** BATAO → MA_TRUST OPEN; Kabir tells Ma everything; Ma gives Papa's service book open at "Ghat route se hataaya gaya — Feb 2001"; in Ep8 he asks «क्या पापा उस रात उसी रूट पर थे?», she deflects and sets «पैसे उन्हीं से लेना जो ख़ुद दें। किसी के आगे हाथ मत फैलाना।». CHHUPAO → MA_TRUST GUARDED; he says he is meeting Papa's friends; that night he overhears Ma at Papa's photo: «तुमने कभी उस लड़की का नाम नहीं लिया, मैं भी नहीं लूँगी।». No ₹/SAATH change either way. Ep8 = #8 Kishore ₹35,000 (2007).

(Old) **What Ep7 needed from the Ep6 result:** ASK → JAMA +₹30,000 (= ₹2,01,000), paid in anger ("ab main karzdaar nahi"); she goes to Ma. LET GO → SAATH +1 (= 2);
she shows her receipt book (each envelope hemmed with a tiny double stitch — image only); she goes to Ma to praise him. Both: Ep7 opens «पापा कहते थे…» (Ma sewed something in 2001).

**What Ep 2 needs from the Ep 1 result:**
- **If ASK won:** the opening says Shankar gave the full ₹6,000 from an old biscuit box, and a Route 47 ticket fell out. COLLECTED becomes ₹6,000 and LET GO stays 0.
- **If LET GO won:** Kabir left Shankar's page alone, and Shankar told him that after one winter Papa stopped drinking chai before his night shift. LET GO becomes 1 and COLLECTED stays ₹0.
- Ep 2 is #2 Pushpa, temple flower seller, ₹14,000 (2004). A pressed jasmine flower falls from her page.

**Prop state:** ledger intact, with Kabir. Bell in the trunk. Trunk at home. Red pen not yet found (that happens in Ep 3).

## 8. Project files (inside the project zip)

| Path | Contents |
|---|---|
| `scripts/` | `art.py` (SVG library, props, ledger, handwriting), `shapes.py` (silhouettes, profiles, hands), `manq.py` (jointed poses), `papa_face.py`, `post.py` (painterly finish), `render.py` (SVG→PNG), `build.sh`, `shots/sNN.py` (one file per shot), and the voice tools (`tts_take.sh`, `gen_takes.sh`, `score*.py`, `asr.py`, `f0.py`, `build_vo.py`) |
| `sound/` | `synth.py`, `score.py`, `mix.py` |
| `edit/` | `edl.py` (shot list and overlays), `render.py` (motion, captions, overlays), `timeline.json` (sound cues), `vo.wav`, `mix.wav`, `vo_lines.json` |
| `vo/` | `script.tsv` (id, pause, speed, Roman, Devanagari), `selected.json` |
| `art/final/` | every finished still (1188×2112) |
| `art/svg/` | every finished still's SVG source |
| `fonts/` | the Google Fonts listed in section 3 |

Each episode lives in its own folder (`ep01/…`) with the same layout: `shots/`, `art/`, `vo/`, `edit/`. Its renderer and shot list live in `epNN/edit/`. The shared libraries stay at the root.
