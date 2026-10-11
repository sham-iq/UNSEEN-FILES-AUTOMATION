#!/usr/bin/env python3
"""Create a daily Unseen Files vertical video without manual uploads."""
import datetime, hashlib, math, os, random, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path("output")
OUT.mkdir(exist_ok=True)
today = datetime.datetime.now(datetime.timezone.utc).date()
stories = [
    {
        "title": "THE PLACE YOUR BRAIN HIDES FEAR",
        "hook": "Your brain can make a threat feel real before you can explain why.",
        "lines": [
            "Your brain is not a camera. It is a prediction machine.",
            "It constantly compares what you see with what it expects to happen.",
            "When something feels uncertain, your threat system can prepare you before you consciously understand the situation.",
            "That is one reason a dark hallway can feel frightening even when you have no evidence that anything is there.",
            "The feeling is real. But the feeling alone is not proof of danger.",
            "Your brain is trying to protect you by guessing what comes next.",
            "Sometimes that guess is useful. Sometimes it is wrong.",
            "The unsettling part is that your mind can create certainty out of incomplete information.",
            "Next time fear appears, pause and ask: what do I know, and what am I imagining?",
            "Follow Unseen Files for more hidden truths about the human mind."
        ],
    },
    {
        "title": "WHY SILENCE FEELS SO LOUD",
        "hook": "In silence, your mind may start searching for things that are not there.",
        "lines": [
            "Have you noticed how a quiet room can suddenly feel uncomfortable?",
            "Your brain is built to notice changes, patterns, and possible threats.",
            "When outside noise disappears, small sounds and thoughts can become much more noticeable.",
            "A ticking clock, a distant creak, even your own breathing can seem unusually loud.",
            "Silence also leaves more room for memories and worries to enter your attention.",
            "That does not mean silence is dangerous. It means your attention has fewer distractions.",
            "Your mind keeps scanning, even when there is nothing urgent to find.",
            "Try sitting quietly for one minute and notice the sounds without inventing a story about them.",
            "Sometimes the mystery is not the room. It is what your brain does with the quiet.",
            "Follow Unseen Files for more strange facts about the mind."
        ],
    },
    {
        "title": "YOUR MEMORY IS NOT A RECORDING",
        "hook": "Every time you remember something, your brain may rebuild parts of it.",
        "lines": [
            "One of the strangest facts about memory is that it is not a perfect recording.",
            "Remembering is an active process. Your brain reconstructs an event from stored details.",
            "Your current mood, later conversations, and new information can influence what feels familiar.",
            "That is why two people can honestly remember the same moment differently.",
            "Confidence does not guarantee accuracy. A vivid memory can still contain mistakes.",
            "This does not mean every memory is false. It means memory is more flexible than we imagine.",
            "The brain is designed to preserve meaning, not every tiny detail like a video file.",
            "When a memory matters, separate what you directly recall from what you later heard.",
            "The past feels fixed. Our access to it is not always so simple.",
            "Follow Unseen Files for more unsettling truths hiding in everyday life."
        ],
    },
    {
        "title": "WHY YOU NOTICE YOUR NAME",
        "hook": "Your attention can pick out personally important words from a noisy room.",
        "lines": [
            "Imagine being surrounded by dozens of conversations.",
            "You are focused on one person, barely hearing anything else.",
            "Then someone across the room says your name, and your attention snaps toward it.",
            "Your brain constantly filters incoming information instead of treating every sound equally.",
            "Words connected to you can be especially important, so they may break through that filter.",
            "Researchers often discuss this as part of selective attention and the cocktail party effect.",
            "It can feel almost supernatural, but it reflects how your attention prioritizes meaningful signals.",
            "You do not hear everything. Your brain chooses what deserves a closer look.",
            "And sometimes, the signal you were waiting for was there all along.",
            "Follow Unseen Files for more hidden psychology and strange facts."
        ],
    },
    {
        "title": "THE FEAR OF BEING WATCHED",
        "hook": "Feeling watched is an experience, not proof that someone is watching.",
        "lines": [
            "Have you ever felt that someone was looking at you, then turned around?",
            "Humans are highly sensitive to social signals and possible threats.",
            "In uncertain situations, your brain can interpret ambiguous cues as meaningful.",
            "A movement in your peripheral vision or a sudden sound can make you check your surroundings.",
            "Sometimes you really have noticed a subtle cue. Other times, your mind has made a cautious guess.",
            "That instinct may help explain why the feeling can arrive before you know what triggered it.",
            "But the sensation alone cannot tell you whether someone is actually watching.",
            "Check the evidence calmly instead of letting the feeling become the evidence.",
            "Your brain is an alert system, not a supernatural detector.",
            "Follow Unseen Files for more mysteries of human perception."
        ],
    },
    {
        "title": "WHY TIME FEELS FASTER",
        "hook": "A year can feel shorter when fewer moments stand out as new.",
        "lines": [
            "Why can childhood summers feel endless while adult years seem to disappear?",
            "There is no single explanation, but memory and novelty may play a role.",
            "New experiences often leave richer, more distinctive memories than repetitive routines.",
            "When you look back, a period filled with memorable firsts can seem longer and fuller.",
            "A routine month may pass normally, yet leave fewer clear landmarks in memory.",
            "That can make the past stretch or shrink depending on what you remember from it.",
            "You cannot stop time, but you can give your days more distinct moments.",
            "Take a different route, learn something unfamiliar, or pay attention to an ordinary detail.",
            "The clock measures time evenly. Your memory does not always describe it that way.",
            "Follow Unseen Files for more hidden truths about everyday life."
        ],
    },
]
story = stories[(today.toordinal() - 1) % len(stories)]
seed = int(hashlib.sha256(str(today).encode()).hexdigest()[:8], 16)
rng = random.Random(seed)

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

W, H = 720, 1280
for i in range(6):
    img = Image.new("RGB", (W, H))
    pix = img.load()
    base = [(7, 10, 19), (18, 10, 23), (6, 18, 27), (19, 13, 12), (7, 10, 20), (13, 9, 22)][i]
    glow_x, glow_y = rng.randint(80, 640), rng.randint(180, 1050)
    glow = (rng.randint(75, 150), rng.randint(12, 35), rng.randint(35, 70))
    for y in range(H):
        for x in range(W):
            d = math.sqrt((x-glow_x)**2 + (y-glow_y)**2)
            k = max(0, 1-d/560) * .5
            noise = rng.randint(-3, 3)
            pix[x,y] = tuple(max(0,min(255,int(base[c]*(1-k)+glow[c]*k+noise))) for c in range(3))
    draw = ImageDraw.Draw(img, "RGBA")
    # atmospheric rings and thin scan lines
    for n in range(8):
        r = 100+n*68+i*8
        draw.ellipse((W//2-r, 470-r, W//2+r, 470+r), outline=(200, 55, 65, max(8,35-n*3)), width=2)
    for y in range(0,H,8):
        draw.line((0,y,W,y), fill=(255,255,255,5), width=1)
    draw.text((52,70), "UNSEEN FILES  /  CASE %03d" % (today.toordinal()%1000), font=font(22,True), fill=(235,65,75,255))
    draw.line((52,118,150,118), fill=(235,65,75,255), width=4)
    if i == 0:
        headline = story["title"]
        body = story["hook"]
        draw.text((52,235), "THE HUMAN MIND", font=font(23,True), fill=(210,210,220,255))
        y0 = 320
        for line in textwrap.wrap(headline, 18):
            draw.text((52,y0), line, font=font(49,True), fill=(248,247,244,255), stroke_width=1, stroke_fill=(0,0,0,180))
            y0 += 65
        y0 += 25
        for line in textwrap.wrap(body, 28):
            draw.text((52,y0), line, font=font(27), fill=(205,208,218,255))
            y0 += 39
    else:
        chunk = story["lines"]
        start = (i-1)*2
        excerpt = " ".join(chunk[start:start+2])
        draw.text((52,260), "FILE NOTE  %02d / 06" % i, font=font(23,True), fill=(235,65,75,255))
        y0 = 365
        for line in textwrap.wrap(excerpt, 30):
            draw.text((52,y0), line, font=font(35,True), fill=(246,245,242,255))
            y0 += 53
        # atmospheric visual motif
        draw.ellipse((220,790,500,1070), outline=(235,65,75,95), width=3)
        draw.ellipse((275,845,445,1015), outline=(235,65,75,65), width=2)
        draw.ellipse((330,900,390,960), fill=(235,65,75,40))
    draw.text((52,1170), "QUESTION EVERYTHING.", font=font(22,True), fill=(230,230,235,230))
    draw.text((52,1210), "FOLLOW  @UNSEENFILES", font=font(17,True), fill=(170,170,185,220))
    img.save(OUT / f"scene{i+1}.png", quality=95)

script_text = " ".join([story["hook"]] + story["lines"])
(OUT / "narration.txt").write_text(script_text, encoding="utf-8")
(OUT / "caption.txt").write_text(
    f"{story['title'].title()}\n\n{story['hook']}\n\nWhat do you think? Follow Unseen Files for disturbing facts, hidden psychology, and mysteries that stay with you.\n\n#UnseenFiles #Psychology #Mysteries #DidYouKnow #HiddenTruths",
    encoding="utf-8")
(OUT / "title.txt").write_text(story["title"], encoding="utf-8")
print(f"Created six cinematic scenes and narration for: {story['title']}")
