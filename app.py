import os
import requests
import json
from flask import Flask, render_template, jsonify
from cachetools import TTLCache

app = Flask(__name__)
cache = TTLCache(maxsize=1, ttl=120)  # Cache for 2 minutes

# -------- COIN METADATA (logos, stories, social links) --------
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

# -------- FETCH REAL DATA FROM COINLORE --------
def fetch_coinlore_data():
    cache_key = 'coinlore'
    if cache_key in cache:
        return cache[cache_key]

    try:
        url = 'https://api.coinlore.net/api/tickers/?start=0&limit=100'
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # Build a dict keyed by symbol (uppercase)
            result = {}
            for item in data.get('data', []):
                symbol = item.get('symbol', '').upper()
                result[symbol] = {
                    'price': float(item.get('price_usd', 0)),
                    'change_24h': float(item.get('percent_change_24h', 0)),
                    'volume': int(item.get('volume24', 0)),
                    'mcap': int(item.get('market_cap_usd', 0))
                }
            cache[cache_key] = result
            return result
    except Exception as e:
        print(f"CoinLore fetch error: {e}")
    return {}

# -------- ROUTES --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard')
def dashboard():
    coinlore = fetch_coinlore_data()
    results = []
    for coin in COINS:
        data = coinlore.get(coin['symbol'].upper(), {})
        price = data.get('price', 0.0)
        change_24h = data.get('change_24h', 0.0)
        volume = data.get('volume', 0)
        mcap = data.get('mcap', 0)
        # Generate a simple sparkline if no real data (CoinLore doesn't provide it)
        sparkline = []
        if price > 0:
            # Simulate a simple trend based on 24h change
            base = price / (1 + change_24h/100)  # approximate starting price
            steps = 10
            for i in range(steps):
                factor = 1 + (change_24h/100) * (i/steps)
                sparkline.append(round(base * factor, 8))
        else:
            sparkline = [0.0] * 10

        # Determine signal based on real change
        if change_24h > 8:
            signal = 'buy'
        elif change_24h < -5:
            signal = 'sell'
        else:
            signal = 'hold'

        hype = 50 + (change_24h * 0.8)  # hype derived from change
        hype = max(10, min(99, int(hype)))

        results.append({
            **coin,
            'price': price,
            'change_24h': round(change_24h, 2),
            'volume': volume,
            'mcap': mcap,
            'sparkline': sparkline,
            'mentions': 0,  # CoinLore doesn't provide mentions
            'hype': hype,
            'signal': signal
        })

    # Sort by hype descending
    results.sort(key=lambda x: x['hype'], reverse=True)
    for idx, coin in enumerate(results):
        coin['rank'] = idx + 1

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)