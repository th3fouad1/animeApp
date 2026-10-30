import os
import sys
import json
import time
import re
import urllib.request
import concurrent.futures
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

sys.stdout.reconfigure(encoding='utf-8')

CARATEEN_KEY = b"7annaba3l_loves_crypto_safe_key!"

# Default output directory: current directory or repo root if passed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT = os.path.dirname(SCRIPT_DIR) # repo root
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", DEFAULT_OUTPUT)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_decrypted(url, retries=3):
    headers = {
        "Referer": "https://carateen.tv/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode('utf-8'))
            
            iv = bytes.fromhex(data['iv'])
            ciphertext = bytes.fromhex(data['encryptedData'])
            
            cipher = Cipher(algorithms.AES(CARATEEN_KEY), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded = decryptor.update(ciphertext) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded) + unpadder.finalize()
            return json.loads(plaintext.decode('utf-8'))
        except Exception:
            if attempt == retries - 1:
                return None
            time.sleep(0.5)
    return None

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\r\n|\r', '\n', str(text))
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def map_genres(category_name, tags="", planet_name=""):
    combined = f"{category_name} {tags} {planet_name}".lower()
    genres = set()
    genres.add("Anime")
    
    if any(k in combined for k in ["أكشن", "قتال", "action", "شعلة"]):
        genres.add("Action")
        genres.add("Shonen")
    if any(k in combined for k in ["مغامر", "adventure", "رحلة"]):
        genres.add("Adventure")
    if any(k in combined for k in ["غموض", "mystery", "تحقيق", "كونان"]):
        genres.add("Mystery")
    if any(k in combined for k in ["كوميد", "comedy", "مضحك", "ضحك"]):
        genres.add("Comedy")
    if any(k in combined for k in ["رياض", "sport", "كرة", "سباق"]):
        genres.add("Sports")
    if any(k in combined for k in ["علم", "sci-fi", "ميكا", "فضاء", "روبوت", "طائرة", "غرندايزر"]):
        genres.add("Sci-Fi")
        genres.add("Mecha")
    if any(k in combined for k in ["زمردة", "بنات", "shojo", "دراما", "حب"]):
        genres.add("Drama")
        genres.add("Shojo")
    if any(k in combined for k in ["سبيستون", "spacetoon", "أيام زمان", "قديمة", "أرشيف", "كلاسيك"]):
        genres.add("Spacetoon")
        genres.add("Nostalgia")
    if any(k in combined for k in ["بون بون", "أطفال", "kids"]):
        genres.add("Kids")
        
    return sorted(list(genres))

def get_actors_catalog():
    return [
        {
            "id": 1,
            "name": "كونان إيدوجاوا (Conan)",
            "photo": "https://cdn.spacetoongo.com/40e0d689-30bf-48aa-b358-d9c2aaf8fa6f.jpg",
            "biography": "سينشي كودو طالب الثانوية ومحقق بارع تقلص جسده ليصبح كونان إيدوجاوا، يحل أصعب القضايا والجرائم بحثاً عن المنظمة السوداء لاستعادة جسده.",
            "birthday": "1994-01-08",
            "place_of_birth": "Tokyo, Japan",
            "known_for_department": "Acting",
            "popularity": 98.5,
            "imdb_id": "nm0174488",
            "movies": [100001, 100024],
            "series": [100453, 100457, 100461, 100465, 100570, 100600, 100762, 100974, 100979, 200959],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "name": "غوكو (Son Goku)",
            "photo": "https://cdn.spacetoongo.com/a4bfbb8e-09e3-4336-b347-ed9a18a77b8e.jpg",
            "biography": "سايان أسطوري نشأ على كوكب الأرض، يتميز بروح المغامرة وحب التدريب وتخطي حدوده لإنقاذ الكون وأصدقائه من أشرس الخصوم.",
            "birthday": "1984-12-03",
            "place_of_birth": "Planet Vegeta",
            "known_for_department": "Acting",
            "popularity": 99.2,
            "imdb_id": "nm0326308",
            "movies": [],
            "series": [101032, 200445, 101039, 101121],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 3,
            "name": "كابتن ماجد (Tsubasa Ozora)",
            "photo": "https://carateen.tv/assets/img/posters/297_cover.webp",
            "biography": "أسطورة كرة القدم وصاحب حلم الفوز بكأس العالم، قائد فريق المجد ومحبوب الملايين في العالم العربي عبر دبلجة سبيستون التاريخية.",
            "birthday": "1983-04-13",
            "place_of_birth": "Shizuoka, Japan",
            "known_for_department": "Acting",
            "popularity": 94.0,
            "imdb_id": "nm0875231",
            "movies": [],
            "series": [100297, 100301, 100305, 100309, 100313],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 4,
            "name": "حسان (Hanamichi Sakuragi)",
            "photo": "https://carateen.tv/assets/img/posters/411_cover.webp",
            "biography": "العبقري ذو الشعر الأحمر وبطل فريق الصقور في كرة السلة، يتميز بحماسته الفائقة وروحه القتالية العالية وقفزاته المذهلة في سلام دانك.",
            "birthday": "1993-10-16",
            "place_of_birth": "Kanagawa, Japan",
            "known_for_department": "Acting",
            "popularity": 92.8,
            "imdb_id": "nm0757271",
            "movies": [],
            "series": [100411, 100415],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 5,
            "name": "غون فريكس (Gon Freecss)",
            "photo": "https://carateen.tv/assets/img/posters/1053_cover.webp",
            "biography": "فتى طيب وطموح يخرج في رحلة ليصبح صياداً محترفاً بحثاً عن والده جينغ فريكس، ويخوض مغامرات حابسة للأنفاس برفقة كيلوا وكورابيكا وليوريو.",
            "birthday": "1999-05-05",
            "place_of_birth": "Whale Island",
            "known_for_department": "Acting",
            "popularity": 96.5,
            "imdb_id": "nm1336402",
            "movies": [],
            "series": [101053],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 6,
            "name": "أمجد وصقر (Tai & Agumon)",
            "photo": "https://cdn.spacetoongo.com/76eafe73-140f-4ac9-b1e2-fee1198fd408.jpg",
            "biography": "قائد أبطال الديجيتال وصاحب شارة الشجاعة، يخوض مع رفيقه صقر معارك مصيرية لإنقاذ العالم الرقمي والعالم الحقيقي.",
            "birthday": "1999-03-07",
            "place_of_birth": "Odaiba, Tokyo",
            "known_for_department": "Acting",
            "popularity": 91.0,
            "imdb_id": "nm0948924",
            "movies": [],
            "series": [100950],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 7,
            "name": "روميو وألفريدو (Romeo & Alfredo)",
            "photo": "https://carateen.tv/assets/img/posters/321_cover.webp",
            "biography": "رمز الصداقة والوفاء في تاريخ كرتون زمان، أبطال منظمة منظفي المداخن في ميلانو الذين حفروا قصتهم في قلوب كل أجيال سبيستون.",
            "birthday": "1995-01-15",
            "place_of_birth": "Switzerland / Italy",
            "known_for_department": "Acting",
            "popularity": 95.0,
            "imdb_id": "nm0739281",
            "movies": [],
            "series": [100321, 201005],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 8,
            "name": "عدنان (Conan / Adnan)",
            "photo": "https://carateen.tv/assets/img/posters/56_cover.webp",
            "biography": "الفتى الشجاع والقوي ذو القدرات الجسدية الخارقة في عالم ما بعد الكارثة، يسعى لإنقاذ لينا من الأسر ومواجهة أطماع القلعة.",
            "birthday": "1978-04-04",
            "place_of_birth": "Remnant Island",
            "known_for_department": "Acting",
            "popularity": 93.4,
            "imdb_id": "nm0594503",
            "movies": [],
            "series": [100056],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 9,
            "name": "سالي كرو (Sara Crewe)",
            "photo": "https://carateen.tv/assets/img/posters/96_cover.webp",
            "biography": "الفتاة النبيلة الصابرة التي واجهت قسوة الحياة في معهد الآنسة منشن بإيمان وأمل وعطف كبير، لتتحول قصتها إلى إحدى أروع كلاسيكيات الأنمي.",
            "birthday": "1985-01-01",
            "place_of_birth": "London, UK",
            "known_for_department": "Acting",
            "popularity": 91.5,
            "imdb_id": "nm0764289",
            "movies": [],
            "series": [100096, 201191],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 10,
            "name": "ماوكلي (Mowgli)",
            "photo": "https://carateen.tv/assets/img/posters/285_cover.webp",
            "biography": "فتى الأدغال الذي ربته الذئاب في الغابة برفقة الدب بالو والفهد باغييرا، وحارب النمر الشرير شريخان لحماية عائلته.",
            "birthday": "1989-10-09",
            "place_of_birth": "Seoni, India",
            "known_for_department": "Acting",
            "popularity": 90.2,
            "imdb_id": "nm0610283",
            "movies": [],
            "series": [100285],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 11,
            "name": "ريمي باربرين (Remi)",
            "photo": "https://carateen.tv/assets/img/posters/482_cover.webp",
            "biography": "الطفلة الشجاعة ذات الصوت العذب والقلب النقي التي جابت فرنسا مع العم فيتاليس وفرقته المتنقلة بحثاً عن والدتها الحقيقية.",
            "birthday": "1996-09-01",
            "place_of_birth": "Chavanon, France",
            "known_for_department": "Acting",
            "popularity": 92.0,
            "imdb_id": "nm0718882",
            "movies": [],
            "series": [100482, 200219],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 12,
            "name": "سندباد (Sindbad)",
            "photo": "https://carateen.tv/assets/img/posters/121_cover.webp",
            "biography": "البحار العربي الشاب التواق للاستكشاف والمغامرة في أعالي البحار، برفقة الطائر ياسمينة والعم حسن وعلي بابا.",
            "birthday": "1975-10-01",
            "place_of_birth": "Baghdad, Iraq",
            "known_for_department": "Acting",
            "popularity": 89.8,
            "imdb_id": "nm0801824",
            "movies": [],
            "series": [100121],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 13,
            "name": "سيباستيان وبيل (Belle and Sebastian)",
            "photo": "https://carateen.tv/assets/img/posters/194_cover.webp",
            "biography": "الفتى الصغير وكلبه الأبيض الوفي العملاق اللذان يخوضان رحلة مشوقة ومؤثرة عبر جبال البرانس بحثاً عن أمه.",
            "birthday": "1981-04-07",
            "place_of_birth": "Pyrenees, France",
            "known_for_department": "Acting",
            "popularity": 88.5,
            "imdb_id": "nm0068402",
            "movies": [],
            "series": [100194],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 14,
            "name": "سنان (Fables of the Green Forest)",
            "photo": "https://carateen.tv/assets/img/posters/206_cover.webp",
            "biography": "القندس الصغير الذكي والمحبوب في الغابة الخضراء، يعيش مغامرات بريئة وجميلة مع أصدقائه ويعلم الصغار حب التعاون والخير.",
            "birthday": "1973-01-07",
            "place_of_birth": "Green Forest",
            "known_for_department": "Acting",
            "popularity": 87.0,
            "imdb_id": "nm0268801",
            "movies": [],
            "series": [100206],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        },
        {
            "id": 15,
            "name": "عامر (Mark Evans / Mamoru Endo)",
            "photo": "https://cdn.spacetoongo.com/dd8074b6-3872-43a1-a80e-0bd436c13e28.jpg",
            "biography": "حارس مرمى وقائد فريق النسور في أبطال الكرة، صاحب اليد السحرية والحماس الملهم الذي لا يعرف الاستسلام أبداً.",
            "birthday": "2008-10-05",
            "place_of_birth": "Inazuma Town, Japan",
            "known_for_department": "Acting",
            "popularity": 94.2,
            "imdb_id": "nm3140921",
            "movies": [],
            "series": [201257, 200891],
            "tmdb_url": None,
            "imported_at": datetime.now().isoformat()
        }
    ]

def run():
    print("🚀 [GitHub Actions / Local] Starting Anime Catalog Sync...")
    print(f"📁 Target Output Directory: {OUTPUT_DIR}")
    
    # 1. Fetch catalogs
    classic_shows = get_decrypted("https://carateen.tv/api/tvshows") or []
    sp_shows = get_decrypted("https://carateen.tv/api/sp/tvshows") or []
    print(f"✓ Found {len(classic_shows)} classic shows & {len(sp_shows)} spacetoon shows")
    
    # 2. Concurrently fetch episodes
    classic_episodes_map = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(get_decrypted, f"https://carateen.tv/api/episodes?id={s['id']}"): s['id'] for s in classic_shows}
        for future in concurrent.futures.as_completed(future_to_id):
            s_id = future_to_id[future]
            try:
                eps = future.result()
                if eps:
                    classic_episodes_map[s_id] = eps
            except Exception:
                pass

    sp_episodes_map = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(get_decrypted, f"https://carateen.tv/api/sp/episodes?id={s['id']}"): s['id'] for s in sp_shows}
        for future in concurrent.futures.as_completed(future_to_id):
            s_id = future_to_id[future]
            try:
                eps = future.result()
                if eps:
                    sp_episodes_map[s_id] = eps
            except Exception:
                pass

    # 3. Transform to Xuper Series & Movies
    all_series = []
    all_movies = []
    trending_mixed = []

    # Classic Shows
    for s in classic_shows:
        s_id = s.get('id')
        title = clean_text(s.get('title'))
        if not title:
            continue
            
        overview = clean_text(s.get('description')) or clean_text(s.get('description_technical'))
        category = s.get('category') or ""
        is_movie = "فيلم" in category or s.get('episodes_count_real') == 1
        
        poster_cover = s.get('poster_cover') or s.get('poster_cover_alt') or ""
        poster_banner = s.get('poster_banner') or s.get('poster_banner_large') or poster_cover
        
        poster_url = f"https://carateen.tv/assets/img/posters/{poster_cover}" if poster_cover else "https://carateen.tv/assets/img/default_cover.webp"
        backdrop_url = f"https://carateen.tv/assets/img/posters/{poster_banner}" if poster_banner else poster_url
        
        year_str = str(s.get('release_year') or "2020")
        year_match = re.search(r'\b(19\d\d|20\d\d)\b', year_str)
        year = int(year_match.group(1)) if year_match else 2020
        first_air_date = f"{year}-01-01"
        
        raw_rating = s.get('rating')
        rating = round(float(raw_rating) * 2, 1) if raw_rating else 8.2
        if rating > 10.0:
            rating = 9.4
        vote_count = int(s.get('total_votes') or max(15, int((s.get('views') or 100) / 30)))
        popularity = float(s.get('views') or 150.0)
        
        genres = map_genres(category, s.get('quality', ''))
        unique_id = 100000 + s_id
        is_featured = popularity > 2000 or any(k in title for k in ["كونان", "غرندايزر", "داي", "سنان", "رعد"])
        
        if is_movie:
            all_movies.append({
                "id": unique_id,
                "type": "movie",
                "adult": False,
                "title": title,
                "original_title": title,
                "tagline": "أنمي كلاسيكي رائع بجودة عالية",
                "overview": overview,
                "poster": poster_url,
                "backdrop": backdrop_url,
                "release_date": first_air_date,
                "year": year,
                "runtime": 90,
                "rating": rating,
                "vote_count": vote_count,
                "popularity": popularity,
                "genres": genres,
                "original_language": "ar",
                "countries": ["JP", "AR"],
                "studios": [],
                "trailer_youtube_key": None,
                "cast": [],
                "featured": is_featured,
                "enabled": True,
                "tmdb_url": None,
                "imported_at": datetime.now().isoformat()
            })
            trending_mixed.append({"type": "movie", "id": unique_id})
        else:
            raw_eps = classic_episodes_map.get(s_id, [])
            episodes_list = []
            for idx, ep in enumerate(raw_eps, start=1):
                ep_id = ep.get('id') or (unique_id * 100 + idx)
                ep_title = clean_text(ep.get('title')) or f"الحلقة {idx}"
                thumb = ep.get('thumbnail')
                still_url = f"https://carateen.tv/assets/img/posters/{thumb}" if thumb else backdrop_url
                episodes_list.append({
                    "id": ep_id,
                    "episode_number": idx,
                    "title": ep_title,
                    "overview": overview[:180] if overview else f"مشاهدة {title} {ep_title} مترجمة ومدبلجة بجودة عالية.",
                    "still": still_url,
                    "runtime": 24,
                    "air_date": first_air_date,
                    "rating": rating
                })
                
            all_series.append({
                "id": unique_id,
                "type": "series",
                "adult": False,
                "title": title,
                "original_title": title,
                "overview": overview,
                "poster": poster_url,
                "backdrop": backdrop_url,
                "first_air_date": first_air_date,
                "year": year,
                "rating": rating,
                "vote_count": vote_count,
                "popularity": popularity,
                "genres": genres,
                "original_language": "ar",
                "countries": ["JP", "AR"],
                "studios": [],
                "trailer_youtube_key": None,
                "cast": [],
                "seasons": [{
                    "season_number": 1,
                    "name": "الموسم 1",
                    "overview": overview,
                    "poster": poster_url,
                    "air_date": first_air_date,
                    "episode_count": len(episodes_list),
                    "episodes": episodes_list
                }],
                "featured": is_featured,
                "enabled": True,
                "tmdb_url": None,
                "imported_at": datetime.now().isoformat()
            })
            trending_mixed.append({"type": "series", "id": unique_id})

    # Spacetoon Shows
    for sp in sp_shows:
        sp_id = sp.get('id')
        name = clean_text(sp.get('name'))
        if not name:
            continue
            
        overview = clean_text(sp.get('pref'))
        is_movie = bool(sp.get('is_movie')) or "فيلم" in name
        
        poster_url = sp.get('cover_full_path') or "https://carateen.tv/assets/img/default_cover.webp"
        backdrop_url = sp.get('trailer_cover_full_path') or poster_url
        
        created_at_str = sp.get('created_at') or "2024-01-01"
        year = 2024
        try:
            year = datetime.fromisoformat(created_at_str.replace("Z", "+00:00")).year
        except Exception:
            pass
        first_air_date = f"{year}-01-01"
        
        popularity = float(sp.get('views') or 300.0)
        rating = 8.8
        vote_count = max(25, int(popularity / 20))
        
        planet_name = sp.get('planet_name') or ""
        tags = sp.get('tags') or ""
        genres = map_genres("سبيستون غو", tags=tags, planet_name=planet_name)
        
        unique_id = 200000 + sp_id
        is_featured = popularity > 3000 or any(k in name for k in ["كونان", "دراغون", "بي باتل", "ون بيس", "أبطال الديجيتال"])
        
        if is_movie:
            all_movies.append({
                "id": unique_id,
                "type": "movie",
                "adult": False,
                "title": name,
                "original_title": name,
                "tagline": f"من أعمال سبيستون غو المميزة - كوكب {planet_name}",
                "overview": overview,
                "poster": poster_url,
                "backdrop": backdrop_url,
                "release_date": first_air_date,
                "year": year,
                "runtime": max(75, int((sp.get('ep_duration') or 5400) / 60)),
                "rating": rating,
                "vote_count": vote_count,
                "popularity": popularity,
                "genres": genres,
                "original_language": "ar",
                "countries": ["JP", "AR"],
                "studios": [],
                "trailer_youtube_key": None,
                "cast": [],
                "featured": is_featured,
                "enabled": True,
                "tmdb_url": None,
                "imported_at": datetime.now().isoformat()
            })
            trending_mixed.append({"type": "movie", "id": unique_id})
        else:
            raw_eps = sp_episodes_map.get(sp_id, [])
            episodes_list = []
            for idx, ep in enumerate(raw_eps, start=1):
                ep_id = ep.get('id') or (unique_id * 100 + idx)
                pref = clean_text(ep.get('pref'))
                ep_title = f"الحلقة {ep.get('number') or idx}"
                if pref:
                    ep_title += f": {pref}"
                still_url = ep.get('cover_full_path') or ep.get('cover') or backdrop_url
                ep_dur = int(ep.get('duration') or ep.get('ep_duration') or 1440)
                runtime_min = max(20, ep_dur // 60)
                episodes_list.append({
                    "id": ep_id,
                    "episode_number": ep.get('number') or idx,
                    "title": ep_title,
                    "overview": pref or f"مشاهدة {name} {ep_title} بدبلجة سبيستون الأصلية بجودة فائقة.",
                    "still": still_url,
                    "runtime": runtime_min,
                    "air_date": first_air_date,
                    "rating": rating
                })
                
            all_series.append({
                "id": unique_id,
                "type": "series",
                "adult": False,
                "title": name,
                "original_title": name,
                "overview": overview,
                "poster": poster_url,
                "backdrop": backdrop_url,
                "first_air_date": first_air_date,
                "year": year,
                "rating": rating,
                "vote_count": vote_count,
                "popularity": popularity,
                "genres": genres,
                "original_language": "ar",
                "countries": ["JP", "AR"],
                "studios": [],
                "trailer_youtube_key": None,
                "cast": [],
                "seasons": [{
                    "season_number": 1,
                    "name": "الموسم 1",
                    "overview": overview,
                    "poster": poster_url,
                    "air_date": first_air_date,
                    "episode_count": len(episodes_list),
                    "episodes": episodes_list
                }],
                "featured": is_featured,
                "enabled": True,
                "tmdb_url": None,
                "imported_at": datetime.now().isoformat()
            })
            trending_mixed.append({"type": "series", "id": unique_id})

    # Sort
    all_series.sort(key=lambda x: x['popularity'], reverse=True)
    all_movies.sort(key=lambda x: x['popularity'], reverse=True)
    
    trending_sorted = []
    for i in range(min(50, max(len(all_series), len(all_movies)))):
        if i < len(all_series):
            trending_sorted.append({"type": "series", "id": all_series[i]['id']})
        if i < len(all_movies):
            trending_sorted.append({"type": "movie", "id": all_movies[i]['id']})

    # Write files
    with open(os.path.join(OUTPUT_DIR, "series.json"), "w", encoding="utf-8") as f:
        json.dump({"series": all_series, "updated_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUTPUT_DIR, "movies.json"), "w", encoding="utf-8") as f:
        json.dump({"movies": all_movies, "updated_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUTPUT_DIR, "trending.json"), "w", encoding="utf-8") as f:
        json.dump({"mixed": trending_sorted}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUTPUT_DIR, "actors.json"), "w", encoding="utf-8") as f:
        json.dump({"actors": get_actors_catalog()}, f, ensure_ascii=False, indent=2)

    print("🎉 [Sync Completed Successfully]")
    print(f"   Series: {len(all_series)} | Movies: {len(all_movies)} | Trending: {len(trending_sorted)}")

if __name__ == "__main__":
    run()
