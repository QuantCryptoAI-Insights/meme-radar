import os
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# -------- COINS (20 coins with realistic base prices) --------
COINS = [
    {"id": "bonk", "name": "Bonk", "symbol": "BONK", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/28600/large/bonk.jpg", "story": "Community-driven dog coin.", "why_popular": "Massive airdrop.", "social": {"twitter": "https://twitter.com/bonk_inu", "website": "https://bonkcoin.com", "telegram": "https://t.me/bonk_sol"}, "category": "Dog Coin", "base_price": 0.00000461},
    {"id": "dogwifhat", "name": "Dogwifhat", "symbol": "WIF", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32588/large/dogwifhat.jpg", "story": "Dog with a hat.", "why_popular": "Iconic branding.", "social": {"twitter": "https://twitter.com/dogwifcoin", "website": "https://dogwifhat.net", "telegram": "https://t.me/dogwifhat"}, "category": "Dog Coin", "base_price": 2.87},
    {"id": "popcat", "name": "Popcat", "symbol": "POPCAT", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/31821/large/popcat.png", "story": "Viral cat meme.", "why_popular": "TikTok presence.", "social": {"twitter": "https://twitter.com/PopcatSolana", "website": "https://popcat.xyz", "telegram": "https://t.me/popcatsol"}, "category": "Animal", "base_price": 1.03},
    {"id": "slerf", "name": "Slerf", "symbol": "SLERF", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32885/large/slerf.jpeg", "story": "Controversial burn.", "why_popular": "Accidental burn story.", "social": {"twitter": "https://twitter.com/SlerfSol", "website": "https://slerf.xyz", "telegram": "https://t.me/slerfsol"}, "category": "Meme", "base_price": 0.042},
    {"id": "myro", "name": "Myro", "symbol": "MYRO", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/31554/large/myro.png", "story": "Solana co-founder's dog.", "why_popular": "First-mover dog meta.", "social": {"twitter": "https://twitter.com/myrosol", "website": "https://myro.meme", "telegram": "https://t.me/myrosol"}, "category": "Dog Coin", "base_price": 0.187},
    {"id": "wen", "name": "Wen", "symbol": "WEN", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32610/large/wen.png", "story": "'Wen Moon?' meme.", "why_popular": "Relatable name.", "social": {"twitter": "https://twitter.com/wencoin", "website": "https://wencoin.xyz", "telegram": "https://t.me/wencoin"}, "category": "Meme", "base_price": 0.00019},
    {"id": "cat-in-a-dogs-world", "name": "Mew", "symbol": "MEW", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/32174/large/mew.png", "story": "Cat in dog world.", "why_popular": "Unique narrative.", "social": {"twitter": "https://twitter.com/MewCoin", "website": "https://mew.xyz", "telegram": "https://t.me/mewcoin"}, "category": "Animal", "base_price": 0.0067},
    {"id": "pepe", "name": "Pepe", "symbol": "PEPE", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/29850/large/pepe-token.jpeg", "story": "Legendary Pepe frog.", "why_popular": "Cultural recognition.", "social": {"twitter": "https://twitter.com/pepecoineth", "website": "https://pepe.vip", "telegram": "https://t.me/pepecoineth"}, "category": "Meme", "base_price": 0.000014},
    {"id": "book-of-meme", "name": "Book of Meme", "symbol": "BOME", "chain": "Solana", "logo": "https://assets.coingecko.com/coins/images/33297/large/bome.jpg", "story": "Art meets crypto.", "why_popular": "Artist backing.", "social": {"twitter": "https://twitter.com/bookofmeme", "website": "https://bookofmeme.xyz", "telegram": "https://t.me/bookofmeme"}, "category": "Art", "base_price": 0.0087},
    {"id": "dogecoin", "name": "Dogecoin", "symbol": "DOGE", "chain": "Dogecoin", "logo": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png", "story": "The original meme coin.", "why_popular": "Elon Musk, oldest meme.", "social": {"twitter": "https://twitter.com/dogecoin", "website": "https://dogecoin.com", "telegram": ""}, "category": "Dog Coin", "base_price": 0.12},
    {"id": "shiba-inu", "name": "Shiba Inu", "symbol": "SHIB", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/11939/large/shiba.png", "story": "The Dogecoin killer.", "why_popular": "Massive ecosystem, Shibarium.", "social": {"twitter": "https://twitter.com/Shibtoken", "website": "https://shibatoken.com", "telegram": ""}, "category": "Dog Coin", "base_price": 0.000023},
    {"id": "floki", "name": "Floki", "symbol": "FLOKI", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/16746/large/Floki.png", "story": "Viking dog named after Elon's pet.", "why_popular": "Strong marketing, utility.", "social": {"twitter": "https://twitter.com/RealFlokiInu", "website": "https://floki.com", "telegram": ""}, "category": "Dog Coin", "base_price": 0.00018},
    {"id": "mog-coin", "name": "Mog", "symbol": "MOG", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/33888/large/mog.png", "story": "The most cat-coded meme.", "why_popular": "Strong cat meta, high conviction.", "social": {"twitter": "https://twitter.com/mogcoineth", "website": "https://mogcoin.com", "telegram": ""}, "category": "Animal", "base_price": 0.000002},
    {"id": "coq-inu", "name": "Coq Inu", "symbol": "COQ", "chain": "Avalanche", "logo": "https://assets.coingecko.com/coins/images/34018/large/coq.png", "story": "Avalanche's first massive meme.", "why_popular": "Avalanche ecosystem hype.", "social": {"twitter": "https://twitter.com/CoqInuAvax", "website": "https://coqinu.com", "telegram": ""}, "category": "Animal", "base_price": 0.000001},
    {"id": "brett", "name": "Brett", "symbol": "BRETT", "chain": "Base", "logo": "https://assets.coingecko.com/coins/images/34434/large/brett.png", "story": "Base Network's best friend.", "why_popular": "Base chain growth.", "social": {"twitter": "https://twitter.com/BrettOnBase", "website": "https://brettbase.com", "telegram": ""}, "category": "Meme", "base_price": 0.09},
    {"id": "toshi", "name": "Toshi", "symbol": "TOSHI", "chain": "Base", "logo": "https://assets.coingecko.com/coins/images/34085/large/toshi.png", "story": "Base Network's original cat.", "why_popular": "Cat meta on Base.", "social": {"twitter": "https://twitter.com/toshithecat", "website": "https://toshithecat.com", "telegram": ""}, "category": "Animal", "base_price": 0.0008},
    {"id": "neiro", "name": "Neiro", "symbol": "NEIRO", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/34641/large/neiro.png", "story": "New dog on the block.", "why_popular": "Successor to DOGE narrative.", "social": {"twitter": "https://twitter.com/NeiroEth", "website": "https://neiroeth.com", "telegram": ""}, "category": "Dog Coin", "base_price": 0.00004},
    {"id": "turbo", "name": "Turbo", "symbol": "TURBO", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/32849/large/turbo.png", "story": "First AI-generated meme coin.", "why_popular": "AI narrative.", "social": {"twitter": "https://twitter.com/TurboToadToken", "website": "https://turbo.xyz", "telegram": ""}, "category": "AI", "base_price": 0.005},
    {"id": "andy", "name": "Andy", "symbol": "ANDY", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/34430/large/andy.png", "story": "Pepe's best friend.", "why_popular": "Pepe ecosystem.", "social": {"twitter": "https://twitter.com/AndyCoin", "website": "https://andycoin.com", "telegram": ""}, "category": "Meme", "base_price": 0.00003},
    {"id": "memecoin", "name": "Memecoin", "symbol": "MEME", "chain": "Ethereum", "logo": "https://assets.coingecko.com/coins/images/28923/large/memecoin.png", "story": "The meme to rule them all.", "why_popular": "9GAG backing.", "social": {"twitter": "https://twitter.com/memecoin", "website": "https://memecoin.com", "telegram": ""}, "category": "Meme", "base_price": 0.00002}
]

# -------- GENERATE SMART SIGNALS --------
def generate_live_data():
    result = []
    for coin in COINS:
        # Random price movement
        price = coin['base_price'] * (1 + random.uniform(-0.04, 0.04))
        change_24h = round(random.uniform(-8, 18), 2)
        
        # Hype score based on change + random factor
        hype = 40 + (change_24h * 0.5) + random.randint(-10, 15)
        hype = max(15, min(99, int(hype)))
        
        # --- SIGNAL LOGIC (gives a mix of BUY, HOLD, SELL) ---
        if change_24h > 8 and hype > 65:
            signal = 'buy'
        elif change_24h > 5 and hype > 55:
            signal = 'buy'
        elif change_24h < -4 and hype < 50:
            signal = 'sell'
        elif change_24h < -6:
            signal = 'sell'
        else:
            signal = 'hold'
        
        # If it's a buy or sell, add extra confidence (for the UI)
        if signal == 'buy':
            signal_label = 'BUY'
        elif signal == 'sell':
            signal_label = 'SELL'
        else:
            signal_label = 'HOLD'
        
        # Generate sparkline
        sparkline = []
        last = price
        for _ in range(10):
            last = last * (1 + random.uniform(-0.02, 0.02))
            sparkline.append(round(last, 10))
        
        result.append({
            **coin,
            'price': round(price, 8),
            'change_24h': change_24h,
            'hype': hype,
            'signal': signal,
            'signal_label': signal_label,
            'risk': random.randint(20, 80),
            'reward': random.randint(20, 80),
            'sparkline': sparkline,
            'volume': int(price * random.randint(1e6, 1e8)),
            'mcap': int(price * random.randint(1e9, 1e11)),
            'mentions': random.randint(100, 5000)
        })
    return result

# -------- ROUTES --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Dashboard running with generated data.'})

@app.route('/api/dashboard')
def dashboard():
    data = generate_live_data()
    # Sort by hype
    data.sort(key=lambda x: x['hype'], reverse=True)
    for idx, coin in enumerate(data):
        coin['rank'] = idx + 1
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)