from datetime import timedelta

from utils.utils import create_single_token

if __name__ == '__main__':
    token, _ = create_single_token({'sub': 'telegram_bot'}, timedelta(weeks=104))
    print(token)
