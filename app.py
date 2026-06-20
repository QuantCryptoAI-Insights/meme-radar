import os
import requests
import statistics
import traceback
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

app = Flask(__name__)

# -------- CACHE --------
cache = TTLCache(maxsize=100, ttl=60)

# -------- CONFIG --------
LUNARCRUSH_KEY = os.getenv('LUNARCRUSH_API_KEY')
TWITTER_BEARER = os.getenv('TWITTER_BEARER_TOKEN')

# -------- COIN DATABASE --------
COINS = [
    {"id": "bonk", "name": "Bonk", "symbol": "BONK", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/28600/large/bonk.jpg", "story": "Community-driven dog coin.", "why_popular": "Massive airdrop.", "social": {"twitter": "https://twitter.com/bonk_inu", "website": "https://bonkcoin.com", "telegram": "https://t.me/bonk_sol"}, "category": "Dog Coin"},
    {"id": "dogwifhat", "name": "Dogwifhat", "symbol": "WIF", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32588/large/dogwifhat.jpg", "story": "Dog with a hat.", "why_popular": "Iconic branding.", "social": {"twitter": "https://twitter.com/dogwifcoin", "website": "https://dogwifhat.net", "telegram": "https://t.me/dogwifhat"}, "category": "Dog Coin"},
    {"id": "popcat", "name": "Popcat", "symbol": "POPCAT", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/31821/large/popcat.png", "story": "Viral cat meme.", "why_popular": "TikTok presence.", "social": {"twitter": "https://twitter.com/PopcatSolana", "website": "https://popcat.xyz", "telegram": "https://t.me/popcatsol"}, "category": "Animal"},
    {"id": "slerf", "name": "Slerf", "symbol": "SLERF", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32885/large/slerf.jpeg", "story": "Controversial burn.", "why_popular": "Accidental burn story.", "social": {"twitter": "https://twitter.com/SlerfSol", "website": "https://slerf.xyz", "telegram": "https://t.me/slerfsol"}, "category": "Meme"},
    {"id": "myro", "name": "Myro", "symbol": "MYRO", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/31554/large/myro.png", "story": "Solana co-founder's dog.", "why_popular": "First-mover dog meta.", "social": {"twitter": "https://twitter.com/myrosol", "website": "https://myro.meme", "telegram": "https://t.me/myrosol"}, "category": "Dog Coin"},
    {"id": "wen", "name": "Wen", "symbol": "WEN", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32610/large/wen.png", "story": "'Wen Moon?' meme.", "why_popular": "Relatable name.", "social": {"twitter": "https://twitter.com/wencoin", "website": "https://wencoin.xyz", "telegram": "https://t.me/wencoin"}, "category": "Meme"},
    {"id": "cat-in-a-dogs-world", "name": "Mew", "symbol": "MEW", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32174/large/mew.png", "story": "Cat in dog world.", "why_popular": "Unique narrative.", "social": {"twitter": "https://twitter.com/MewCoin", "website": "https://mew.xyz", "telegram": "https://t.me/mewcoin"}, "category": "Animal"},
    {"id": "pepe", "name": "Pepe", "symbol": "PEPE", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/29850/large/pepe-token.jpeg", "story": "Legendary Pepe frog.", "why_popular": "Cultural recognition.", "social": {"twitter": "https://twitter.com/pepecoineth", "website": "https://pepe.vip", "telegram": "https://t.me/pepecoineth"}, "category": "Meme"},
    {"id": "book-of-meme", "name": "Book of Meme", "symbol": "BOME", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/33297/large/bome.jpg", "story": "Art meets crypto.", "why_popular": "Artist backing.", "social": {"twitter": "https://twitter.com/bookofmeme", "website": "https://bookofmeme.xyz", "telegram": "https://t.me/bookofmeme"}, "category": "Art"},
    {"id": "dogecoin", "name": "Dogecoin", "symbol": "DOGE", "chain": "Dogecoin", "logo": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png", "story": "The original meme coin.", "why_popular": "Elon Musk, oldest meme.", "social": {"twitter": "https://twitter.com/dogecoin", "website": "https://dogecoin.com", "telegram": ""}, "category": "Dog Coin"},
    {"id": "shiba-inu", "name": "Shiba Inu", "symbol": "SHIB", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/11939/large/shiba.png", "story": "The Dogecoin killer.", "why_popular": "Massive ecosystem, Shibarium.", "social": {"twitter": "https://twitter.com/Shibtoken", "website": "https://shibatoken.com", "telegram": ""}, "category": "Dog Coin"},
    {"id": "floki", "name": "Floki", "symbol": "FLOKI", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/16746/large/Floki.png", "story": "Viking dog named after Elon's pet.", "why_popular": "Strong marketing, utility.", "social": {"twitter": "https://twitter.com/RealFlokiInu", "website": "https://floki.com", "telegram": ""}, "category": "Dog Coin"},
    {"id": "mog-coin", "name": "Mog", "symbol": "MOG", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/33888/large/mog.png", "story": "The most cat-coded meme.", "why_popular": "Strong cat meta, high conviction.", "social": {"twitter": "https://twitter.com/mogcoineth", "website": "https://mogcoin.com", "telegram": ""}, "category": "Animal"},
    {"id": "coq-inu", "name": "Coq Inu", "symbol": "COQ", "chain": "Avalanche", "logo": "https://assets.coingecko.com/coins/images/34018/large/coq.png", "story": "Avalanche's first massive meme.", "why_popular": "Avalanche ecosystem hype.", "social": {"twitter": "https://twitter.com/CoqInuAvax", "website": "https://coqinu.com", "telegram": ""}, "category": "Animal"},
    {"id": "brett", "name": "Brett", "symbol": "BRETT", "chain": "Base", "logo": "https://assets.coingecko.com/coins/images/34434/large/brett.png", "story": "Base Network's best friend.", "why_popular": "Base chain growth.", "social": {"twitter": "https://twitter.com/BrettOnBase", "website": "https://brettbase.com", "telegram": ""}, "category": "Meme"},
    {"id": "toshi", "name": "Toshi", "symbol": "TOSHI", "chain": "Base", "logo": "https://assets.coingecko.com/coins/images/34085/large/toshi.png", "story": "Base Network's original cat.", "why_popular": "Cat meta on Base.", "social": {"twitter": "https://twitter.com/toshithecat", "website": "https://toshithecat.com", "telegram": ""}, "category": "Animal"},
    {"id": "neiro", "name": "Neiro", "symbol": "NEIRO", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/34641/large/neiro.png", "story": "New dog on the block.", "why_popular": "Successor to DOGE narrative.", "social": {"twitter": "https://twitter.com/NeiroEth", "website": "https://neiroeth.com", "telegram": ""}, "category": "Dog Coin"},
    {"id": "turbo", "name": "Turbo", "symbol": "TURBO", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/32849/large/turbo.png", "story": "First AI-generated meme coin.", "why_popular": "AI narrative.", "social": {"twitter": "https://twitter.com/TurboToadToken", "website": "https://turbo.xyz", "telegram": ""}, "category": "AI"},
    {"id": "andy", "name": "Andy", "symbol": "ANDY", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/34430/large/andy.png", "story": "Pepe's best friend.", "why_popular": "Pepe ecosystem.", "social": {"twitter": "https://twitter.com/AndyCoin", "website": "https://andycoin.com", "telegram": ""}, "category": "Meme"},
    {"id": "memecoin", "name": "Memecoin", "symbol": "MEME", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/28923/large/memecoin.png", "story": "The meme to rule them all.", "why_popular": "9GAG backing.", "social": {"twitter": "https://twitter.com/memecoin", "website": "https://memecoin.com", "telegram": ""}, "category": "Meme"}
]

# -------- FETCH FUNCTIONS --------
def get_coingecko_data():
    cache_key = 'coingecko'
    if cache_key in cache:
        return cache[cache_key]

    ids = ','.join([c['id'] for c in COINS])
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={ids}&order=market_cap_desc&per_page=250&page=1&sparkline=true'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"Fetching CoinGecko data for {len(COINS)} coins...")
        resp = requests.get(url, timeout=15, headers=headers)
        print(f"CoinGecko response status: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print(f"CoinGecko returned {len(data)} coins")
            result = {item['id']: item for item in data}
            cache[cache_key] = result
            return result
        else:
            print(f"CoinGecko returned status {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
    except Exception as e:
        print(f"CoinGecko Error: {e}")
        import traceback
        traceback.print_exc()

    return {}

def get_twitter_mentions(symbol):
    if not TWITTER_BEARER:
        return None
    cache_key = f'twitter_{symbol}'
    if cache_key in cache:
        return cache[cache_key]
    query = f'${symbol} -is:retweet lang:en'
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=public_metrics'
    headers = {'Authorization': f'Bearer {TWITTER_BEARER}'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            count = data.get('meta', {}).get('result_count', 0)
            cache[cache_key] = count
            return count
    except Exception as e:
        print(f"Twitter Error for {symbol}: {e}")
    return None

# ---------- FIXED: Returns 3 values correctly ----------
def calculate_risk_reward(sparkline, price, change_24h):
    """Calculate Risk, Reward, and 7-day change."""
    # Default return values (3 values)
    if not sparkline or len(sparkline) < 7:
        return 50, 50, 0  # risk, reward, change_7d

    # 7-day change
    change_7d = ((sparkline[-1] - sparkline[0]) / sparkline[0]) * 100 if sparkline[0] > 0 else 0

    # Volatility
    returns = []
    for i in range(1, len(sparkline)):
        if sparkline[i-1] > 0:
            returns.append((sparkline[i] - sparkline[i-1]) / sparkline[i-1])
    volatility = statistics.stdev(returns) * 100 if len(returns) > 1 else 2.0

    risk_score = min(99, max(1, int(volatility * 15)))
    reward_raw = (change_24h * 0.6) + (change_7d * 0.4)
    reward_score = min(99, max(1, int(50 + reward_raw * 1.5)))

    # THIS MUST RETURN 3 VALUES
    return risk_score, reward_score, change_7d

# -------- ROUTES --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard')
def dashboard():
    cg_data = get_coingecko_data()
    raw_results = []

    for coin in COINS:
        cg = cg_data.get(coin['id'], {})
        price = cg.get('current_price', 0.0)
        change_24h = cg.get('price_change_percentage_24h', 0.0) or 0.0
        volume = cg.get('total_volume', 0)
        mcap = cg.get('market_cap', 0)
        sparkline = cg.get('sparkline_in_7d', {}).get('price', [])

        twitter_count = get_twitter_mentions(coin['symbol'])
        mentions = twitter_count if twitter_count is not None else 0

        # This call expects 3 values back
        risk_score, reward_score, change_7d = calculate_risk_reward(sparkline, price, change_24h)

        raw_hype = 50 + (change_24h * 0.5) + (change_7d * 0.3)

        raw_results.append({
            **coin,
            'price': price,
            'change_24h': round(change_24h, 2),
            'change_7d': round(change_7d, 2),
            'volume': volume,
            'mcap': mcap,
            'sparkline': sparkline[-10:] if sparkline else [],
            'mentions': mentions,
            'risk': risk_score,
            'reward': reward_score,
            'raw_hype': raw_hype
        })

    raw_results.sort(key=lambda x: x['raw_hype'], reverse=True)

    final_results = []
    total = len(raw_results)

    for idx, coin in enumerate(raw_results):
        hype_score = max(35, 95 - (idx * 8))
        hype_score += (idx % 3) - 1
        hype_score = max(10, min(99, round(hype_score)))

        if idx < total * 0.3:
            signal = 'buy'
        elif idx > total * 0.7:
            signal = 'sell'
        else:
            signal = 'hold'

        final_results.append({
            'rank': idx + 1,
            **coin,
            'hype': hype_score,
            'signal': signal
        })

    return jsonify(final_results)

@app.route('/api/top_gainers')
def top_gainers():
    data = dashboard().get_json()
    sorted_data = sorted(data, key=lambda x: x.get('change_24h', 0), reverse=True)
    return jsonify(sorted_data[:3])

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🚀 MemeRadar Pro v3.0 starting...")
    print(f"📊 Loaded {len(COINS)} coins")
    print(f"🔗 Access on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)