import json


def process_accepted(message, field):
    return dict(
        desired=dict(
            value=message.get('state', {}).get('desired', {}).get(field),
            timestamp=message.get('metadata', {}).get('desired', {}).get(field, {}).get('timestamp'),
        ),
        reported=dict(
            value=message.get('state', {}).get('reported', {}).get(field),
            timestamp=message.get('metadata', {}).get('reported', {}).get(field, {}).get('timestamp'),
        ),
        timestamp=message.get('timestamp'),
        version=message.get('version'),
        client_token=message.get('clientToken')
    )


def process_delta(message, field):
    return dict(
        desired=dict(
            value=message['state'].get(field),
            timestamp=message['metadata'].get(field, {}).get('timestamp'),
        ),
        reported=dict(
            value=None,
            timestamp=None,
        ),
        timestamp=message['timestamp'],
        version=message['version'],
        client_token=message.get('clientToken')
    )


def process_documents(message, field):
    return dict(
        desired=dict(
            value=message['current']['state'].get('desired', {}).get(field),
            timestamp=message['current']['metadata'].get('desired', {}).get(field, {}).get('timestamp'),
        ),
        reported=dict(
            value=message['current']['state']['reported'].get(field),
            timestamp=message['current']['metadata']['reported'].get(field, {}).get('timestamp'),
        ),
        timestamp=message['timestamp'],
        version=message['current']['version'],
        client_token=message.get('clientToken')
    )


def mystr(s):
    if s is None:
        return ''
    return str(s)


def compose_csv(timestamp, topic, data):
    output = [
        mystr(timestamp),
        topic,
        mystr(data['timestamp']),
        mystr(data['version']),
        mystr(data['desired']['value']),
        mystr(data['desired']['timestamp']),
        mystr(data['reported']['value']),
        mystr(data['reported']['timestamp']),
        mystr(data['client_token']),
    ]
    return ",".join(output)


def process_file(name, field):
    with open(name) as f:
        for line in f.readlines():
            timestamp, topic, message = line.split(' ', 2)
            topic = topic[31:]
            message = json.loads(message)
            if message == "":
                message = {}

            if topic in ('get/accepted', 'update/accepted', 'update'):
                data = process_accepted(message, field)
            elif topic in ('update/delta',):
                data = process_delta(message, field)
            elif topic in ('update/documents',):
                data = process_documents(message, field)
            elif topic in ('get',):
                data = process_accepted(message, field)
            else:
                print(topic, message)
            print(compose_csv(timestamp, topic, data))


if __name__ == '__main__':
    process_file("../data/aws-log-1614928973.txt", "jetstreamState")
