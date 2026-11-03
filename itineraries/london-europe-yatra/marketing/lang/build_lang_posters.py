"""
Telugu, Hindi, Kannada and Tamil versions of the designer's London Europe Yatra
poster. poster_base.png (from make_base.py) keeps the photos, logos, country
pictures and footer; this script writes each language on top in the same places.

    python3 marketing/lang/make_base.py && python3 marketing/lang/build_lang_posters.py
    node marketing/lang/render_lang.cjs
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = {
    "te": ("Noto Serif Telugu", "Noto Sans Telugu"),
    "hi": ("Noto Serif Devanagari", "Noto Sans Devanagari"),
    "kn": ("Noto Serif Kannada", "Noto Sans Kannada"),
    "ta": ("Noto Serif Tamil", "Noto Sans Tamil"),
}

T = {
    "te": dict(
        name="Telugu", title1="లండన్ యూరప్", title2="యాత్ర",
        sub="హరే కృష్ణ భక్తులతో 8 దేశాల యాత్ర",
        dates="ఏప్రిల్ 17 – మే 2 | 15 రాత్రులు / 16 రోజులు",
        amount="యాత్ర మొత్తం", incl="(అంతర్జాతీయ విమాన టిక్కెట్లతో సహా)",
        seats=["*పరిమిత సీట్లు –", "ముందు వచ్చిన వారికి ముందు"],
        countries=["యునైటెడ్ కింగ్‌డమ్", "ఫ్రాన్స్", "బెల్జియం", "నెదర్లాండ్స్", "వాటికన్ సిటీ", "జర్మనీ", "స్విట్జర్లాండ్", "ఇటలీ"],
        holy_h="పవిత్ర క్షేత్రాలు",
        holy="ఇస్కాన్ ప్యారిస్, రాధాదేశ్ (బెల్జియం), ఇస్కాన్ కొలోన్, గోలోక ధామ్ (జర్మనీ), ఇస్కాన్ జ్యూరిచ్, విల్లాజియో హరే కృష్ణ (ఇటలీ), ప్రభుపాద దేశ్ (ఇటలీ), విల్లా వృందావన్ (ఫ్లోరెన్స్), అక్షయ పాత్ర వంటశాల (వాట్‌ఫోర్డ్)",
        wonders_h="యూరప్ అద్భుతాలు",
        wonders="చేంజింగ్ ఆఫ్ ది గార్డ్ & టవర్ ఆఫ్ లండన్ (కోహినూర్), లండన్ ఐ & థేమ్స్ నదీ విహారం, ఈఫిల్ టవర్, లూవ్ర్ & సీన్ నదీ విహారం, కూకెన్‌హోఫ్ తులిప్ తోటలు & డచ్ గాలిమరలు, మౌంట్ టిట్లిస్ మంచు & లూసర్న్ సరస్సు, రైన్ జలపాతం & బ్లాక్ ఫారెస్ట్, వెనిస్ గోండోలా విహారం, వాటికన్, సిస్టీన్ చాపెల్ & కొలోసియం, ఫ్లోరెన్స్ & పీసా వాలు గోపురం",
        exp="ఆధ్యాత్మిక యాత్రలో మీకు లభించేవి",
        features=["మధురమైన భజనలు & కీర్తనలు", "స్థల పురాణ కథనాలు (తెలుగు / హిందీ / ఇంగ్లీష్)", "సౌకర్యవంతమైన బస",
                  "విశ్రాంతికరమైన ప్రయాణ ప్రణాళిక", "వృద్ధులకు ప్రత్యేక శ్రద్ధ", "సాత్విక ఆహారం",
                  "వైదిక ఆటలు & బహుమతులు", "వివిధ పురాణాల నుండి ఆలయ కథలు"],
        tag="ప్రపంచంలో అత్యంత విశ్వసనీయ ధార్మిక యాత్రా నిపుణులు",
    ),
    "hi": dict(
        name="Hindi", title1="लंदन यूरोप", title2="यात्रा",
        sub="हरे कृष्ण भक्तों के साथ 8 देशों की यात्रा",
        dates="17 अप्रैल – 2 मई | 15 रातें / 16 दिन",
        amount="यात्रा राशि", incl="(अंतरराष्ट्रीय उड़ान टिकट सहित)",
        seats=["*सीमित सीटें –", "पहले आओ, पहले पाओ"],
        countries=["यूनाइटेड किंगडम", "फ़्रांस", "बेल्जियम", "नीदरलैंड्स", "वेटिकन सिटी", "जर्मनी", "स्विट्ज़रलैंड", "इटली"],
        holy_h="पवित्र तीर्थ",
        holy="इस्कॉन पेरिस, राधादेश (बेल्जियम), इस्कॉन कोलोन, गोलोक धाम (जर्मनी), इस्कॉन ज़्यूरिख, विलाज्जो हरे कृष्ण (इटली), प्रभुपाद देश (इटली), विला वृंदावन (फ़्लोरेंस), अक्षय पात्र रसोई (वॉटफ़र्ड)",
        wonders_h="यूरोप के अजूबे",
        wonders="चेंजिंग ऑफ़ द गार्ड और टावर ऑफ़ लंदन (कोहिनूर), लंदन आई और टेम्स नदी की सैर, एफ़िल टावर, लूव्र और सीन नदी की सैर, क्यूकेनहॉफ़ ट्यूलिप बाग़ और डच पवनचक्कियाँ, माउंट टिटलिस की बर्फ़ और ल्यूसर्न झील, राइन जलप्रपात और ब्लैक फ़ॉरेस्ट, वेनिस में गोंडोला की सवारी, वेटिकन, सिस्टीन चैपल और कोलोसियम, फ़्लोरेंस और पीसा की झुकी मीनार",
        exp="आध्यात्मिक यात्रा का अनुभव करें",
        features=["मधुर भजन और कीर्तन", "स्थल पुराण कथाएँ (तेलुगु / हिंदी / अंग्रेज़ी)", "आरामदायक ठहराव",
                  "आरामदायक यात्रा कार्यक्रम", "वरिष्ठ नागरिकों की विशेष देखभाल", "सात्विक भोजन",
                  "वैदिक खेल और उपहार", "विभिन्न पुराणों से मंदिर कथाएँ"],
        tag="विश्व के सबसे विश्वसनीय धार्मिक यात्रा विशेषज्ञ",
    ),
    "kn": dict(
        name="Kannada", title1="ಲಂಡನ್ ಯುರೋಪ್", title2="ಯಾತ್ರೆ",
        sub="ಹರೇ ಕೃಷ್ಣ ಭಕ್ತರೊಂದಿಗೆ 8 ದೇಶಗಳ ಯಾತ್ರೆ",
        dates="ಏಪ್ರಿಲ್ 17 – ಮೇ 2 | 15 ರಾತ್ರಿಗಳು / 16 ದಿನಗಳು",
        amount="ಯಾತ್ರೆಯ ಮೊತ್ತ", incl="(ಅಂತರರಾಷ್ಟ್ರೀಯ ವಿಮಾನ ಟಿಕೆಟ್‌ಗಳು ಸೇರಿ)",
        seats=["*ಸೀಮಿತ ಸೀಟುಗಳು –", "ಮೊದಲು ಬಂದವರಿಗೆ ಮೊದಲ ಆದ್ಯತೆ"],
        countries=["ಯುನೈಟೆಡ್ ಕಿಂಗ್‌ಡಮ್", "ಫ್ರಾನ್ಸ್", "ಬೆಲ್ಜಿಯಂ", "ನೆದರ್‌ಲ್ಯಾಂಡ್ಸ್", "ವ್ಯಾಟಿಕನ್ ಸಿಟಿ", "ಜರ್ಮನಿ", "ಸ್ವಿಟ್ಜರ್‌ಲ್ಯಾಂಡ್", "ಇಟಲಿ"],
        holy_h="ಪವಿತ್ರ ಕ್ಷೇತ್ರಗಳು",
        holy="ಇಸ್ಕಾನ್ ಪ್ಯಾರಿಸ್, ರಾಧಾದೇಶ್ (ಬೆಲ್ಜಿಯಂ), ಇಸ್ಕಾನ್ ಕಲೋನ್, ಗೋಲೋಕ ಧಾಮ್ (ಜರ್ಮನಿ), ಇಸ್ಕಾನ್ ಜ್ಯೂರಿಕ್, ವಿಲ್ಲಾಜಿಯೋ ಹರೇ ಕೃಷ್ಣ (ಇಟಲಿ), ಪ್ರಭುಪಾದ ದೇಶ್ (ಇಟಲಿ), ವಿಲ್ಲಾ ವೃಂದಾವನ (ಫ್ಲಾರೆನ್ಸ್), ಅಕ್ಷಯ ಪಾತ್ರ ಅಡುಗೆಮನೆ (ವಾಟ್‌ಫರ್ಡ್)",
        wonders_h="ಯುರೋಪಿನ ಅದ್ಭುತಗಳು",
        wonders="ಚೇಂಜಿಂಗ್ ಆಫ್ ದಿ ಗಾರ್ಡ್ ಮತ್ತು ಟವರ್ ಆಫ್ ಲಂಡನ್ (ಕೊಹಿನೂರ್), ಲಂಡನ್ ಐ ಮತ್ತು ಥೇಮ್ಸ್ ನದಿ ವಿಹಾರ, ಐಫೆಲ್ ಟವರ್, ಲೂವ್ರ್ ಮತ್ತು ಸೀನ್ ನದಿ ವಿಹಾರ, ಕ್ಯೂಕೆನ್‌ಹಾಫ್ ಟುಲಿಪ್ ತೋಟಗಳು ಮತ್ತು ಡಚ್ ಗಾಳಿಯಂತ್ರಗಳು, ಮೌಂಟ್ ಟಿಟ್ಲಿಸ್ ಹಿಮ ಮತ್ತು ಲೂಸರ್ನ್ ಸರೋವರ, ರೈನ್ ಜಲಪಾತ ಮತ್ತು ಬ್ಲ್ಯಾಕ್ ಫಾರೆಸ್ಟ್, ವೆನಿಸ್ ಗೊಂಡೋಲಾ ವಿಹಾರ, ವ್ಯಾಟಿಕನ್, ಸಿಸ್ಟೀನ್ ಚಾಪೆಲ್ ಮತ್ತು ಕೊಲೊಸಿಯಮ್, ಫ್ಲಾರೆನ್ಸ್ ಮತ್ತು ಪೀಸಾದ ವಾಲುವ ಗೋಪುರ",
        exp="ಆಧ್ಯಾತ್ಮಿಕ ಯಾತ್ರೆಯಲ್ಲಿ ಅನುಭವಿಸಿ",
        features=["ಮಧುರ ಭಜನೆಗಳು ಮತ್ತು ಕೀರ್ತನೆಗಳು", "ಸ್ಥಳ ಪುರಾಣ ನಿರೂಪಣೆ (ತೆಲುಗು / ಹಿಂದಿ / ಇಂಗ್ಲಿಷ್)", "ಆರಾಮದಾಯಕ ವಸತಿ",
                  "ನಿರಾಳವಾದ ಪ್ರಯಾಣ ಯೋಜನೆ", "ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ವಿಶೇಷ ಕಾಳಜಿ", "ಸಾತ್ವಿಕ ಆಹಾರ",
                  "ವೈದಿಕ ಆಟಗಳು ಮತ್ತು ಉಡುಗೊರೆಗಳು", "ವಿವಿಧ ಪುರಾಣಗಳಿಂದ ದೇವಾಲಯದ ಕಥೆಗಳು"],
        tag="ವಿಶ್ವದ ಅತ್ಯಂತ ವಿಶ್ವಾಸಾರ್ಹ ಧಾರ್ಮಿಕ ಪ್ರವಾಸ ತಜ್ಞರು",
    ),
    "ta": dict(
        name="Tamil", title1="லண்டன் ஐரோப்பா", title2="யாத்திரை",
        sub="ஹரே கிருஷ்ண பக்தர்களுடன் 8 நாடுகள் யாத்திரை",
        dates="ஏப்ரல் 17 – மே 2 | 15 இரவுகள் / 16 நாட்கள்",
        amount="யாத்திரைக் கட்டணம்", incl="(சர்வதேச விமான டிக்கெட்டுகள் உட்பட)",
        seats=["*குறைந்த இருக்கைகள் –", "முதலில் வருபவருக்கே முன்னுரிமை"],
        countries=["ஐக்கிய இராச்சியம்", "பிரான்ஸ்", "பெல்ஜியம்", "நெதர்லாந்து", "வாடிகன் நகரம்", "ஜெர்மனி", "சுவிட்சர்லாந்து", "இத்தாலி"],
        holy_h="புனிதத் தலங்கள்",
        holy="இஸ்கான் பாரிஸ், ராதாதேஷ் (பெல்ஜியம்), இஸ்கான் கொலோன், கோலோக தாம் (ஜெர்மனி), இஸ்கான் சூரிக், வில்லாஜியோ ஹரே கிருஷ்ணா (இத்தாலி), பிரபுபாத தேஷ் (இத்தாலி), வில்லா விருந்தாவன் (ஃப்ளோரன்ஸ்), அட்சய பாத்திரா சமையலறை (வாட்ஃபோர்டு)",
        wonders_h="ஐரோப்பாவின் அதிசயங்கள்",
        wonders="சேஞ்சிங் ஆஃப் தி கார்டு & டவர் ஆஃப் லண்டன் (கோஹினூர்), லண்டன் ஐ & தேம்ஸ் நதி உலா, ஈஃபிள் கோபுரம், லூவ்ர் & சீன் நதி உலா, கியூகென்ஹாஃப் டூலிப் தோட்டங்கள் & டச்சு காற்றாலைகள், டிட்லிஸ் மலைப் பனி & லூசர்ன் ஏரி, ரைன் நீர்வீழ்ச்சி & பிளாக் ஃபாரஸ்ட், வெனிஸ் கோண்டோலா பயணம், வாடிகன், சிஸ்டைன் சேப்பல் & கொலோசியம், ஃப்ளோரன்ஸ் & பைசா சாய்ந்த கோபுரம்",
        exp="ஆன்மிக யாத்திரையில் அனுபவியுங்கள்",
        features=["இனிய பஜனைகள் & கீர்த்தனைகள்", "ஸ்தல புராண விளக்கங்கள் (தெலுங்கு / இந்தி / ஆங்கிலம்)", "வசதியான தங்குமிடம்",
                  "நிதானமான பயணத் திட்டம்", "மூத்த குடிமக்களுக்குச் சிறப்புக் கவனிப்பு", "சாத்வீக உணவு",
                  "வேத விளையாட்டுகள் & பரிசுகள்", "பல்வேறு புராணங்களிலிருந்து கோயில் கதைகள்"],
        tag="உலகின் மிக நம்பகமான ஆன்மிகப் பயண நிபுணர்கள்",
    ),
}

# country label strips on the base image: (left, top) in px, each 174 × 26
TILES = [(44, 1072), (229, 1072), (412, 1072), (597, 1072), (44, 1233), (229, 1233), (412, 1233), (597, 1233)]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1131px;height:1600px;position:relative;overflow:hidden;background:url('poster_base.png') 0 0/1131px 1600px no-repeat;font-family:'SANS',sans-serif}
.a{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center}
.fit{white-space:nowrap}
.title::before{content:'';position:absolute;inset:0 40px;background:radial-gradient(ellipse at center,rgba(255,226,170,.92) 0%,rgba(255,226,170,.75) 45%,rgba(255,226,170,0) 72%);z-index:-1}
.title{left:120px;width:891px;top:128px;height:192px;flex-direction:column;font-family:'SERIF',serif;font-weight:800;color:#7A0E0B;line-height:1.0;text-shadow:0 2px 0 rgba(255,236,190,.9),0 0 18px rgba(255,236,190,.95)}
.title .l1{font-size:78px} .title .l2{font-size:84px}
html[lang=hi] .title{line-height:.92} html[lang=hi] .title .l1{font-size:84px} html[lang=hi] .title .l2{font-size:96px}
.sub{left:150px;width:831px;top:318px;height:34px;font-weight:800;font-size:23px;color:#2a0a05;text-shadow:0 0 8px rgba(255,236,190,1),0 0 4px rgba(255,236,190,1)}
.pill{left:215px;width:701px;top:354px;height:58px;border-radius:30px;background:linear-gradient(180deg,#9E1712,#6A0907);border:2px solid #C9932F;color:#fff;font-weight:700;font-size:25px;box-shadow:0 6px 14px rgba(0,0,0,.35);padding:0 18px}
.badge{left:424px;width:300px;top:724px;height:140px;border-radius:22px;background:linear-gradient(135deg,#F7E3A1 0%,#E6BF5C 45%,#C9932F 100%);border:3px solid #FFF0B8;box-shadow:0 6px 18px rgba(0,0,0,.45);flex-direction:column;padding:6px 10px}
.badge .l{font-family:'SERIF',serif;font-weight:700;color:#7A0E0B;font-size:30px;line-height:1.25}
.badge .v{font-family:Inter,sans-serif;font-weight:900;color:#1b0c05;font-size:54px;line-height:1.1}
.incl{left:330px;width:470px;top:870px;height:58px;flex-direction:column;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.8)}
.incl .i{font-size:17px;font-weight:600} .incl .g{font-size:16px;margin-top:3px}
.seats{left:26px;width:298px;top:874px;height:50px;border-radius:12px;background:linear-gradient(135deg,#F7E3A1,#D9A84A);border:2px solid #FFF0B8;color:#1b0c05;flex-direction:column;font-weight:800;font-size:14px;line-height:1.25;padding:0 8px}
.lab{width:174px;height:26px;background:linear-gradient(180deg,#4A1A04,#2E0E01);color:#F4CF74;font-weight:700;font-size:14px;padding:0 4px}
.right{left:776px;width:355px;top:936px;height:336px;background:linear-gradient(180deg,#0E0A08,#0A0705);flex-direction:column;justify-content:flex-start;padding:10px 12px 0}
.h{display:inline-block;background:linear-gradient(180deg,#F7E3A1,#D9A84A);color:#5A0806;font-family:'SERIF',serif;font-weight:800;font-size:15px;border-radius:14px;padding:2px 16px;margin:6px 0}
.txt{color:#fff;font-size:12.6px;line-height:1.62;font-weight:600}
.bottom{left:0;width:1131px;top:1280px;height:178px;background:#120801;flex-direction:column;padding:0 40px}
.exp{font-family:'SERIF',serif;color:#E9C46A;font-weight:800;font-size:22px;letter-spacing:.02em}
.orn{color:#C9932F;font-size:12px;margin:2px 0 6px;letter-spacing:4px}
.feat{width:100%;color:#fff;font-size:17px;line-height:1.75;font-weight:500}
.feat span{white-space:nowrap;margin:0 7px}
.feat b{color:#F6B81B;margin-right:4px}
.tag{left:108px;width:874px;top:1466px;height:66px;border-radius:34px;background:linear-gradient(180deg,#F26B1D,#C8410B);border:2px solid #FFD19A;color:#fff;font-family:'SERIF',serif;font-weight:800;font-size:30px;box-shadow:0 4px 10px rgba(0,0,0,.35);padding:0 24px}
"""

FIT_JS = """
<script>
document.fonts.ready.then(()=>{
  for (const el of document.querySelectorAll('[data-fit]')) {
    let s = parseFloat(getComputedStyle(el).fontSize);
    const box = el.closest('.a') || el;
    while ((el.scrollWidth > box.clientWidth - 4 || box.scrollHeight > box.clientHeight + 1) && s > 8) { s -= 0.5; el.style.fontSize = s + 'px'; }
  }
  // title lines: fit the width only, so tall scripts are not shrunk for line height
  for (const el of document.querySelectorAll('[data-fitw]')) {
    let s = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > 880 && s > 20) { s -= 1; el.style.fontSize = s + 'px'; }
  }
  // shrink grouped blocks together so both lists keep the same size
  const groups = {};
  for (const el of document.querySelectorAll('[data-group]')) (groups[el.dataset.group] ||= []).push(el);
  for (const els of Object.values(groups)) {
    const box = els[0].closest('.a');
    let s = parseFloat(getComputedStyle(els[0]).fontSize);
    while (box.scrollHeight > box.clientHeight + 1 && s > 8) { s -= 0.25; els.forEach(e => e.style.fontSize = s + 'px'); }
  }
  document.body.dataset.ready = '1';
});
</script>"""


def page(code):
    t = T[code]
    serif, sans = FONTS[code]
    fam = "&family=".join(f.replace(" ", "+") + ":wght@400;500;600;700;800;900" for f in (serif, sans))
    css = CSS.replace("'SERIF'", f"'{serif}'").replace("'SANS'", f"'{sans}'")
    labs = "".join(f'<div class="a lab" style="left:{x}px;top:{y}px"><span class="fit" data-fit>{c}</span></div>'
                   for (x, y), c in zip(TILES, t["countries"]))
    feats = " ".join(f'<span><b>★</b>{f}</span>' for f in t["features"])
    return f"""<!doctype html><html lang="{code}"><head><meta charset="utf-8"><title>London Europe Yatra – {t['name']}</title>
<link href="https://fonts.googleapis.com/css2?family={fam}&family=Inter:wght@600;800;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="a title"><div class="l1 fit" data-fitw>{t['title1']}</div><div class="l2 fit" data-fitw>{t['title2']}</div></div>
<div class="a sub"><span class="fit" data-fit>{t['sub']}</span></div>
<div class="a pill"><span class="fit" data-fit>{t['dates']}</span></div>
<div class="a badge"><div class="l fit" data-fit>{t['amount']}</div><div class="v">₹5,49,000</div></div>
<div class="a incl"><div class="i fit" data-fit>{t['incl']}</div><div class="g">+ 5% GST, + 2% TCS</div></div>
<div class="a seats"><div class="fit" data-fit>{t['seats'][0]}</div><div class="fit" data-fit>{t['seats'][1]}</div></div>
{labs}
<div class="a right"><div class="h">{t['holy_h']}</div><div class="txt" data-group="r">{t['holy']}</div>
<div class="h" style="margin-top:10px">{t['wonders_h']}</div><div class="txt" data-group="r">{t['wonders']}</div></div>
<div class="a bottom"><div class="exp fit" data-fit>{t['exp']}</div><div class="orn">◆ ─── ◆ ─── ◆</div><div class="feat" data-fit>{feats}</div></div>
<div class="a tag"><span class="fit" data-fit>{t['tag']}</span></div>
{FIT_JS}
</body></html>"""


def main():
    for code in T:
        with open(os.path.join(HERE, f"poster_{code}.html"), "w", encoding="utf-8") as f:
            f.write(page(code))
    print("wrote", ", ".join(f"poster_{c}.html" for c in T))


if __name__ == "__main__":
    main()
