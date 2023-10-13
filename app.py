import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Function to add or update a player's score
def update_score(player, score):
    redis_client.zadd('leaderboard', {player: score})

# Function to get the leaderboard with top N players
def get_leaderboard(limit=10):
    leaderboard = redis_client.zrevrangebyscore('leaderboard', '+inf', '-inf', start=0, num=limit, withscores=True)
    return [(player.decode(), score) for player, score in leaderboard]

# Example Usage
update_score('Player1', 1000)
update_score('Player2', 1500)
update_score('Player3', 1200)
update_score('Player4', 800)

top_players = get_leaderboard()
print("Top Players:")
for player, score in top_players:
    print(f"{player}: {score}")
