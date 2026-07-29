from collections import deque

MAX_HISTORY = 10

history = deque(maxlen=MAX_HISTORY)


def add_message(role, content):

    history.append(
        {
            "role": role,
            "content": content
        }
    )


def get_history():

    return list(history)


def clear_history():

    history.clear()