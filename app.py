import os
import requests
import statistics
import traceback
import time
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=120)

# -------- COINS (20 coins) --------
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

# -------- FETCH COINGECKO DATA (USING PROXY) --------
def get_coingecko_data():
    cache_key = 'coingecko'
    if cache_key in cache:
        return cache[cache_key]

    result = {}
    
    # Build the CoinGecko URL
    ids = ','.join([c['id'] for c in COINS])
    coin_gecko_url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true'
    
    # Try through CORS proxy (Render-friendly)
    proxy_url = f'https://corsproxy.io/?{coin_gecko_url}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"Fetching prices via proxy for {len(COINS)} coins...")
        resp = requests.get(proxy_url, timeout=15, headers=headers)
        print(f"Proxy status: {resp.status_code}")
        
        if resp.status_code == 200:
            price_data = resp.json()
            for coin_id, data in price_data.items():
                result[coin_id] = {
                    'id': coin_id,
                    'current_price': data.get('usd', 0.0),
                    'price_change_percentage_24h': data.get('usd_24h_change', 0.0),
                    'market_cap': data.get('usd_market_cap', 0),
                    'total_volume': data.get('usd_24h_vol', 0),
                    'sparkline_in_7d': {'price': []}
                }
            print(f"Got prices for {len(result)} coins via proxy")
        else:
            print(f"Proxy failed: {resp.status_code}")
    except Exception as e:
        print(f"Proxy error: {e}")
        traceback.print_exc()

    # If proxy fails, try direct CoinGecko (might work sometimes)
    if not result:
        try:
            print("Trying direct CoinGecko...")
            resp = requests.get(coin_gecko_url, timeout=10, headers=headers)
            if resp.status_code == 200:
                price_data = resp.json()
                for coin_id, data in price_data.items():
                    result[coin_id] = {
                        'id': coin_id,
                        'current_price': data.get('usd', 0.0),
                        'price_change_percentage_24h': data.get('usd_24h_change', 0.0),
                        'market_cap': data.get('usd_market_cap', 0),
                        'total_volume': data.get('usd_24h_vol', 0),
                        'sparkline_in_7d': {'price': []}
                    }
                print(f"Got prices for {len(result)} coins directly")
        except Exception as e:
            print(f"Direct CoinGecko error: {e}")

    # Get sparklines (only for top coins, to avoid rate limits)
    if result:
        sparkline_coins = ['bonk', 'dogwifhat', 'popcat', 'slerf', 'myro', 'wen', 'pepe', 'dogecoin', 'shiba-inu']
        for coin_id in sparkline_coins:
            if coin_id not in result:
                continue
            try:
                chart_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=7'
                proxy_chart_url = f'https://corsproxy.io/?{chart_url}'
                resp = requests.get(proxy_chart_url, timeout=10, headers=headers)
                if resp.status_code == 200:
                    chart_data = resp.json()
                    prices = [p[1] for p in chart_data.get('prices', [])]
                    result[coin_id]['sparkline_in_7d'] = {'price': prices}
                    print(f"Got sparkline for {coin_id} ({len(prices)} points)")
                else:
                    print(f"Sparkline failed for {coin_id}: {resp.status_code}")
                time.sleep(0.3)
            except Exception as e:
                print(f"Sparkline error for {coin_id}: {e}")

        cache[cache_key] = result
        print(f"Cached {len(result)} coins")
    else:
        print("No data fetched from CoinGecko")

    return result

# -------- UTILITY FUNCTIONS --------
def calculate_risk_reward(sparkline, price, change_24h):
    if not sparkline or len(sparkline) < 7:
        return 50, 50, 0
    change_7d = ((sparkline[-1] - sparkline[0]) / sparkline[0]) * 100 if sparkline[0] > 0 else 0
    returns = []
    for i in range(1, len(sparkline)):
        if sparkline[i-1] > 0:
            returns.append((sparkline[i] - sparkline[i-1]) / sparkline[i-1])
    volatility = statistics.stdev(returns) * 100 if len(returns) > 1 else 2.0
    risk_score = min(99, max(1, int(volatility * 15)))
    reward_raw = (change_24h * 0.6) + (change_7d * 0.4)
    reward_score = min(99, max(1, int(50 + reward_raw * 1.5)))
    return risk_score, reward_score, change_7d

# -------- ROUTES --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bonk&vs_currencies=usd'
        proxy_url = f'https://corsproxy.io/?{url}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(proxy_url, timeout=10, headers=headers)
        return jsonify({
            'status': resp.status_code,
            'data': resp.json() if resp.status_code == 200 else resp.text
        })
    except Exception as e:
        return jsonify({'error': str(e)})

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

        mentions = 0

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)